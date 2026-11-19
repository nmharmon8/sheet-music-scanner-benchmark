"""
Scores a run by the music it writes down, not by how its MusicXML is laid out: our own diagnostic, beside the official
TEDn (score.py). Two encodings of the same printed music score zero here.

Elements are placed in time, so it ignores voice numbers, backup/forward, hidden rests, chord order and divisions. The
measures are lined up three ways and the one with the fewest errors counts (music.md says how often each won):
  bars           our measures matched to the gold's by their pitches (extra or missing measures cost what is in
                 them and a barline each); onset within the measure in quarter notes
  bar-fraction   the same, onset and length as a fraction of the measure: 9/8 in eighths and 3/4 in triplet eighths,
                 which print almost alike, read as the same music
  system-onset   onset in quarter notes from the start of the system: a barline in the wrong place (one measure read
                 as two) costs one barline, not every note after it
Compared:

  notes        onset, pitch, length, grace; a note right but for its length, accidental or octave is one error of
               that kind, as is the right pitch in the right measure at the wrong time (wrong rhythm); otherwise
               missing or extra. On matched notes: staff, ties, articulations/ornaments, slurs.
  rests        visible rests: onset, length, staff
  clefs, key   the clef/key in force at the start of the system and where it changes
  time         only where the gold prints one: a crop from mid-piece shows none, and the time we carry is context
  barlines     where measures end inside the system, and repeat/double styles
  dynamics     marks (p, f, ...) and hairpin starts, by onset

Not compared, but counted: stems, beams and tuplet brackets ("not predicted": the export draws standard stems and
beams), and voice numbers (no effect on the music).

    olimpic/.venv/bin/python -I olimpic/music_score.py <label> [more labels] [--worst n]

Writes runs/<label>/music.json and music.md.
"""
import collections, json, os, sys
import xml.etree.ElementTree as ET
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data', 'olimpic-1.0-scanned')
ARTICS = {'staccato', 'accent', 'tenuto', 'staccatissimo', 'strong-accent', 'trill-mark', 'mordent', 'inverted-mordent',
          'turn', 'fermata'}
DYNAMICS = {'p', 'pp', 'ppp', 'pppp', 'f', 'ff', 'fff', 'ffff', 'mp', 'mf', 'sf', 'sfz', 'sfp', 'fp', 'rf', 'rfz', 'fz', 'sffz'}


def piano_part(root):
    parts = root.findall('part')
    for p in parts:
        if any(s.text and s.text.strip() == '2' for s in p.iter('staves')):
            return p
    return parts[-1] if parts else None


def num(el, tag, default=None):
    c = el.find(tag)
    return c.text.strip() if c is not None and c.text else default


def extract(xml_text):
    """The music of the piano part: notes, rests, clefs, keys, times, barlines, dynamics, engraving counts."""
    out = {k: [] for k in ('notes', 'rests', 'clefs', 'keys', 'times', 'bars', 'barstyles', 'dynamics')}
    out['measures'] = 0
    out['mlen'] = []
    out['engraving'] = collections.Counter()
    if not xml_text:
        return out
    part = piano_part(ET.fromstring(xml_text))
    if part is None:
        return out
    divisions, start = 1, Fraction(0)
    clef_now, key_now, time_now = {}, None, None
    measures = part.findall('measure')
    out['measures'] = len(measures)
    for mi, m in enumerate(measures):
        pos = maxpos = Fraction(0)
        at = lambda local: (start + local, (mi, local))
        prev_onset = Fraction(0)
        for el in m:
            if el.tag == 'attributes':
                divisions = int(num(el, 'divisions', divisions))
                k = el.find('key')
                if k is not None and num(k, 'fifths') is not None:
                    f = int(num(k, 'fifths'))
                    if f != key_now:
                        out['keys'].append((at(pos), f))
                        key_now = f
                t = el.find('time')
                if t is not None and num(t, 'beats'):
                    v = f"{num(t, 'beats')}/{num(t, 'beat-type')}"
                    if v != time_now:
                        out['times'].append((at(pos), v))
                        time_now = v
                for c in el.findall('clef'):
                    staff = int(c.get('number', '1'))
                    v = f"{num(c, 'sign')}{num(c, 'line', '')}{num(c, 'clef-octave-change', '')}"
                    if clef_now.get(staff) != v:
                        out['clefs'].append((at(pos), staff, v))
                        clef_now[staff] = v
            elif el.tag == 'note':
                grace = el.find('grace') is not None
                chord = el.find('chord') is not None
                dur = Fraction(0) if grace else Fraction(int(num(el, 'duration', '0')), divisions)
                onset = prev_onset if chord else pos
                staff = int(num(el, 'staff', '1'))
                if el.find('stem') is not None:
                    out['engraving']['stems'] += 1
                out['engraving']['beams'] += len(el.findall('beam'))
                notations = el.find('notations')
                if notations is not None:
                    out['engraving']['tuplet brackets'] += len(notations.findall('tuplet'))
                rest = el.find('rest')
                if rest is not None:
                    if el.get('print-object') != 'no':
                        out['rests'].append({'onset': at(onset), 'dur': dur, 'staff': staff})
                elif el.find('pitch') is not None:
                    p = el.find('pitch')
                    n = {'onset': at(onset), 'step': num(p, 'step'), 'alter': int(float(num(p, 'alter', '0'))),
                         'octave': int(num(p, 'octave')), 'dur': dur, 'grace': grace, 'staff': staff,
                         'tie': any(t.get('type') == 'start' for t in el.findall('tie')), 'artics': set(), 'slur': set()}
                    if notations is not None:
                        n['tie'] = n['tie'] or any(t.get('type') == 'start' for t in notations.findall('tied'))
                        for group in ('articulations', 'ornaments'):
                            g = notations.find(group)
                            if g is not None:
                                n['artics'] |= {c.tag for c in g if c.tag in ARTICS}
                        if notations.find('fermata') is not None:
                            n['artics'].add('fermata')
                        n['slur'] = {s.get('type') for s in notations.findall('slur') if s.get('type') in ('start', 'stop')}
                    out['notes'].append(n)
                if not chord:
                    prev_onset = pos
                    pos += dur
            elif el.tag == 'backup':
                pos -= Fraction(int(num(el, 'duration', '0')), divisions)
            elif el.tag == 'forward':
                pos += Fraction(int(num(el, 'duration', '0')), divisions)
            elif el.tag == 'direction':
                here = at(pos + Fraction(int(num(el, 'offset', '0')), divisions))
                for dt in el.findall('direction-type'):
                    for d in dt.findall('dynamics'):
                        out['dynamics'] += [(here, c.tag) for c in d if c.tag in DYNAMICS]
                    for w in dt.findall('wedge'):
                        if w.get('type') in ('crescendo', 'diminuendo'):
                            out['dynamics'].append((here, w.get('type')))
            elif el.tag == 'barline':
                style = num(el, 'bar-style', '')
                rep = el.find('repeat')
                kind = f"repeat-{rep.get('direction')}" if rep is not None else style if style in ('light-light', 'light-heavy', 'heavy-light') else None
                if kind:
                    out['barstyles'].append(kind)
            maxpos = max(maxpos, pos)
        start += maxpos
        out['mlen'].append(maxpos)
        if mi < len(measures) - 1:
            out['bars'].append(start)
    return out


def multiset_diff(gold, pred):
    g, p = collections.Counter(gold), collections.Counter(pred)
    return sum((g - p).values()), sum((p - g).values())


def align_measures(gold, pred):
    """Pred measure index -> gold measure index, by edit distance over each measure's pitches (Needleman-Wunsch).
    An unmatched measure maps to nothing: its contents are extra or missing, and it costs one barline."""
    def pitches(side):
        out = [collections.Counter() for _ in range(side['measures'])]
        for x in side['notes']:
            out[x['onset'][1][0]][(x['step'], x['alter'], x['octave'])] += 1
        return out
    g, p = pitches(gold), pitches(pred)
    G, P = len(g), len(p)
    gap = lambda c: sum(c.values()) + 1
    INF = float('inf')
    D = [[INF] * (P + 1) for _ in range(G + 1)]
    D[0][0] = 0
    for i in range(G + 1):
        for j in range(P + 1):
            if i and D[i - 1][j] + gap(g[i - 1]) < D[i][j]:
                D[i][j] = D[i - 1][j] + gap(g[i - 1])
            if j and D[i][j - 1] + gap(p[j - 1]) < D[i][j]:
                D[i][j] = D[i][j - 1] + gap(p[j - 1])
            if i and j:
                c = D[i - 1][j - 1] + sum(((g[i - 1] - p[j - 1]) + (p[j - 1] - g[i - 1])).values())
                if c < D[i][j]:
                    D[i][j] = c
    mapping, i, j, gaps = {}, G, P, 0
    while i or j:
        if i and j and D[i][j] == D[i - 1][j - 1] + sum(((g[i - 1] - p[j - 1]) + (p[j - 1] - g[i - 1])).values()):
            mapping[j - 1] = i - 1; i -= 1; j -= 1
        elif i and D[i][j] == D[i - 1][j] + gap(g[i - 1]):
            gaps += 1; i -= 1
        else:
            gaps += 1; j -= 1
    return mapping, gaps


def compare(gold, pred):
    """The fewest errors over three ways of lining the measures up (see the module doc), and gold counts."""
    mapping, gaps = align_measures(gold, pred)
    best = None
    for method in ('bars', 'bar-fraction', 'system-onset'):
        e, n = compare_with(gold, pred, method, mapping, gaps)
        if best is None or sum(e.values()) < sum(best[0].values()):
            best = (e, n, method)
    return best


def compare_with(gold, pred, method, mapping, gaps):
    e = collections.Counter()
    n = collections.Counter()

    def placer(side, is_pred):
        def bar(mi):
            return (mapping.get(mi, ('unmatched', mi))) if is_pred else mi
        def where(a):
            (absolute, (mi, local)) = a
            if method == 'system-onset':
                return absolute
            if method == 'bar-fraction':
                return (bar(mi), local / side['mlen'][mi] if side['mlen'][mi] else local)
            return (bar(mi), local)
        def length(a, dur):
            mi = a[1][0]
            return dur / side['mlen'][mi] if method == 'bar-fraction' and side['mlen'][mi] else dur
        return where, length

    gw, gl = placer(gold, False)
    pw, pl = placer(pred, True)
    notes = lambda side, w, l: [{**x, 'onset': w(x['onset']), 'dur': l(x['onset'], x['dur']), 'bar': w(x['onset'])[0] if method != 'system-onset' else None} for x in side['notes']]
    gn, pn = notes(gold, gw, gl), notes(pred, pw, pl)
    n['notes'] = len(gn)
    matched = []
    stages = [('exact', lambda x: (x['onset'], x['step'], x['alter'], x['octave'], x['dur'], x['grace'])),
              ('wrong length', lambda x: (x['onset'], x['step'], x['alter'], x['octave'])),
              ('wrong accidental', lambda x: (x['onset'], x['step'], x['octave'])),
              ('wrong octave', lambda x: (x['onset'], x['step'], x['alter']))]
    if method != 'system-onset':  # the right note in the right measure, at the wrong time: one rhythm error
        stages.append(('wrong rhythm', lambda x: (x['bar'], x['step'], x['alter'], x['octave'])))
    for stage, key in stages:
        index = collections.defaultdict(list)
        for x in pn:
            index[key(x)].append(x)
        rest_g = []
        for x in gn:
            if index[key(x)]:
                # of identical candidates, the one that agrees most (two voices can sound the same note)
                cands = index[key(x)]
                y = max(cands, key=lambda c: (c['staff'] == x['staff']) + (c['tie'] == x['tie']) + (c['artics'] == x['artics']) + (c['slur'] == x['slur']))
                cands.remove(y)
                matched.append((x, y))
                if stage != 'exact':
                    e[stage] += 1
            else:
                rest_g.append(x)
        used = {id(y) for _, y in matched}
        gn, pn = rest_g, [x for x in pn if id(x) not in used]
    e['missing notes'] += len(gn)
    e['extra notes'] += len(pn)
    for x, y in matched:
        e['wrong staff'] += x['staff'] != y['staff']
        e['ties'] += x['tie'] != y['tie']
        e['articulations'] += len(x['artics'] ^ y['artics'])
        e['slurs'] += len(x['slur'] ^ y['slur'])
    for x in gn:  # marks on notes we missed
        e['ties'] += x['tie']
        e['articulations'] += len(x['artics'])
        e['slurs'] += len(x['slur'])
    n['ties'] = sum(x['tie'] for x in gold['notes'])
    n['articulations'] = sum(len(x['artics']) for x in gold['notes'])
    n['slurs'] = sum(len(x['slur']) for x in gold['notes'])
    placed = lambda xs, w: [(w(x[0]), *x[1:]) for x in xs]
    rests = lambda side, w, l: [(w(r['onset']), l(r['onset'], r['dur']), r['staff']) for r in side['rests']]
    simple = {
        'rests': (rests(gold, gw, gl), rests(pred, pw, pl)),
        'clefs': (placed(gold['clefs'], gw), placed(pred['clefs'], pw)),
        'key': (placed(gold['keys'], gw), placed(pred['keys'], pw)),
        'dynamics': (placed(gold['dynamics'], gw), placed(pred['dynamics'], pw)),
    }
    gold_times = placed(gold['times'], gw)
    first = gw(((Fraction(0)), (0, Fraction(0))))
    pred_times = [t for t in placed(pred['times'], pw) if t[0] != first or any(g[0] == first for g in gold_times)]
    simple['time'] = (gold_times, pred_times)
    for k, (g, p) in simple.items():
        miss, extra = multiset_diff(g, p)
        e[k] += miss + extra
        n[k] = len(g)
    miss, extra = multiset_diff(gold['barstyles'], pred['barstyles'])
    if method == 'system-onset':
        m2, x2 = multiset_diff(gold['bars'], pred['bars'])
        miss, extra = miss + m2, extra + x2
    else:
        e['barlines'] += gaps
    e['barlines'] += miss + extra
    n['barlines'] = len(gold['bars']) + len(gold['barstyles'])
    return e, n


NOTE_ERRORS = ['missing notes', 'extra notes', 'wrong rhythm', 'wrong length', 'wrong accidental', 'wrong octave']
ON_NOTES = ['wrong staff', 'ties', 'articulations', 'slurs']
OTHER = ['rests', 'clefs', 'key', 'time', 'barlines', 'dynamics']


def main():
    args = sys.argv[1:]
    worst_n = int(args[args.index('--worst') + 1]) if '--worst' in args else 10
    labels = [a for i, a in enumerate(args) if not a.startswith('--') and (i == 0 or args[i - 1] != '--worst')]
    for label in labels:
        run_dir = os.path.join(HERE, 'runs', label)
        ids = json.load(open(os.path.join(run_dir, 'run.json')))['ids']
        E, N, G_eng, P_eng, methods = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
        per = []
        for s in ids:
            gold = extract(open(os.path.join(DATA, s + '.musicxml')).read())
            f = os.path.join(run_dir, s, 'prediction.musicxml')
            pred = extract(open(f).read() if os.path.exists(f) else '')
            e, n, method = compare(gold, pred)
            methods[method] += 1
            E += e; N += n; G_eng += gold['engraving']; P_eng += pred['engraving']
            ne = sum(e[k] for k in NOTE_ERRORS)
            per.append({'id': s, 'noteErrors': ne, 'notes': n['notes'], 'noteErrorRate': round(100 * ne / max(1, n['notes']), 1),
                        'allErrors': sum(e.values()), 'alignment': method, 'errors': dict(e)})
        note_err = sum(E[k] for k in NOTE_ERRORS)
        all_err, all_gold = sum(E.values()), sum(N.values())
        exact_systems = sum(1 for p in per if p['allErrors'] == 0)
        note_exact = sum(1 for p in per if p['noteErrors'] == 0)
        pct = lambda a, b: f'{100 * a / b:.1f}%' if b else '–'
        md = [f'# Music score · {label}', '',
              f'{len(ids)} systems · **note error rate {pct(note_err, N["notes"])}** ({note_err} of {N["notes"]} gold notes) · '
              f'all marks {pct(all_err, all_gold)} · systems with every note right {note_exact} · with everything right {exact_systems}', '',
              '| category | errors | gold | rate |', '|---|---:|---:|---:|']
        md += [f'| {k} | {E[k]} | {N["notes"]} | {pct(E[k], N["notes"])} |' for k in NOTE_ERRORS]
        md += [f'| {k} (on notes) | {E[k]} | {N[k] if k != "wrong staff" else N["notes"]} | {pct(E[k], N[k] if k != "wrong staff" else N["notes"])} |' for k in ON_NOTES]
        md += [f'| {k} | {E[k]} | {N[k]} | {pct(E[k], N[k])} |' for k in OTHER]
        md += ['', 'Measures lined up by: ' + ', '.join(f'{k} {v}' for k, v in methods.most_common()),
               '', 'Not predicted or not compared (engraving): ' + ', '.join(f'{k}: gold {G_eng[k]}, ours {P_eng[k]}' for k in ('stems', 'beams', 'tuplet brackets')), '',
               f'## Worst {worst_n} systems by note errors', '']
        for p in sorted(per, key=lambda p: -p['noteErrorRate'])[:worst_n]:
            md.append(f"- `{p['id']}`: {p['noteErrors']}/{p['notes']} notes ({p['noteErrorRate']}%) · "
                      + ', '.join(f'{k} {v}' for k, v in sorted(p['errors'].items(), key=lambda kv: -kv[1]) if v))
        json.dump({'label': label, 'errors': dict(E), 'gold': dict(N), 'noteErrorRate': round(100 * note_err / max(1, N['notes']), 2),
                   'allMarksErrorRate': round(100 * all_err / max(1, all_gold), 2), 'noteExactSystems': note_exact,
                   'exactSystems': exact_systems, 'alignment': dict(methods), 'engraving': {'gold': dict(G_eng), 'ours': dict(P_eng)}, 'perSystem': per},
                  open(os.path.join(run_dir, 'music.json'), 'w'), indent=1, default=str)
        open(os.path.join(run_dir, 'music.md'), 'w').write('\n'.join(md) + '\n')
        print('\n'.join(md) + '\n')


if __name__ == '__main__':
    main()
