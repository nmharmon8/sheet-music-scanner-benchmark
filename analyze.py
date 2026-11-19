"""
Inspects every tool's MusicXML exports in results/ (no answer keys needed except I's) and writes results/analysis.json:

- per export: measures, pitched notes, grace notes, and counts of the notation it kept (fingering, lyrics, chord
  symbols, repeats, endings, jumps, dynamics, articulations, ornaments, pedal, tuplets, ties, clef/key/time changes);
- I (Shenandoah) scored against keys/shenandoah-lead-sheet.musicxml: measures exactly right, note F1 (pitch, and
  pitch + duration), chord symbols, lyrics per verse, jump marks;
- stability: how many of a tool's measures on a scan come out identical on the same page's photos/screenshot;
- agreement: share of identical measures between every pair of tools on the scans.

These are provisional until A-H and J have keys: stability and agreement are not accuracy.

    python3 -I analyze.py
"""
import csv, json, os, re, sys, zipfile
import xml.etree.ElementTree as ET
from fractions import Fraction
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, 'results')
INDEX = json.load(open(os.path.join(HERE, 'index.json')))
IDS = [u['id'] for u in INDEX['uploads']]
STEP = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
VARIANTS = {'A': ['A2', 'A3'], 'C': ['C2', 'C3'], 'G': ['G2', 'G3'], 'D': ['D2']}


def local(tag):
    return tag.rsplit('}', 1)[-1]


def load(path):
    if path.endswith('.mxl'):
        z = zipfile.ZipFile(path)
        name = next(n for n in z.namelist() if n.endswith('.xml') and not n.startswith('META-INF'))
        root = ET.fromstring(z.read(name))
    else:
        root = ET.parse(path).getroot()
    for el in root.iter():
        el.tag = local(el.tag)
    return root


def parse(path):
    root = load(path)
    feat = {k: 0 for k in ['fingering', 'lyrics', 'chords', 'repeats', 'endings', 'segno', 'coda', 'dacapo', 'dalsegno',
                           'fine', 'tocoda', 'dynamics', 'articulations', 'ornaments', 'pedal', 'tuplets', 'ties',
                           'slurs', 'fermatas', 'grace', 'clef_changes', 'key_changes', 'time_changes', 'words']}
    measures = {}  # measure index -> list of (onset, midi, dur, staff)
    lengths, nominal, fingers = {}, {}, []  # measure index -> actual length, time-signature length (quarters); (measure, onset, midi, finger)
    harmonies, lyrics_by_verse, words = [], {}, []
    parts = root.findall('part')
    for pi, part in enumerate(parts):
        div = 1
        meter = Fraction(4)
        seen_attr = {'clef': 0, 'key': 0, 'time': 0}
        for mi, m in enumerate(part.findall('measure')):
            t = Fraction(0)
            mlen = Fraction(0)
            last_onset = Fraction(0)
            evs = measures.setdefault(mi, [])
            for tm in m.iter('time'):
                b, bt = tm.findtext('beats'), tm.findtext('beat-type')
                if b and bt and '+' not in b:
                    meter = Fraction(int(b) * 4, int(bt))
            nominal[mi] = max(nominal.get(mi, 0), meter)
            for el in m:
                tag = el.tag
                if tag == 'attributes':
                    if el.find('divisions') is not None:
                        div = int(float(el.find('divisions').text))
                    for k in ('clef', 'key', 'time'):
                        n = len(el.findall(k))
                        if n:
                            if seen_attr[k]:
                                feat[k + '_changes'] += 1
                            seen_attr[k] += n
                elif tag == 'backup':
                    t -= Fraction(int(float(el.find('duration').text)), div)
                elif tag == 'forward':
                    t += Fraction(int(float(el.find('duration').text)), div)
                    mlen = max(mlen, t)
                elif tag == 'harmony':
                    r = el.find('root')
                    if r is not None:
                        alter = r.findtext('root-alter') or '0'
                        b = el.find('bass')
                        bass = (b.findtext('bass-step') + ('#' if (b.findtext('bass-alter') or '0').startswith('1') else 'b' if (b.findtext('bass-alter') or '0').startswith('-') else '')) if b is not None else ''
                        harmonies.append((mi, r.findtext('root-step') + {'1': '#', '-1': 'b'}.get(alter.split('.')[0], ''), norm_kind(el.findtext('kind') or ''), bass))
                        feat['chords'] += 1
                elif tag == 'direction':
                    for w in el.iter('words'):
                        if w.text and w.text.strip():
                            words.append(w.text.strip())
                            feat['words'] += 1
                    feat['segno'] += len(list(el.iter('segno')))
                    feat['coda'] += len(list(el.iter('coda')))
                    feat['dynamics'] += len(list(el.iter('dynamics')))
                    feat['pedal'] += len(list(el.iter('pedal')))
                    s = el.find('sound')
                    if s is not None:
                        for a, k in (('dacapo', 'dacapo'), ('dalsegno', 'dalsegno'), ('fine', 'fine'), ('tocoda', 'tocoda')):
                            if s.get(a) is not None:
                                feat[k] += 1
                elif tag == 'barline':
                    feat['repeats'] += len(el.findall('repeat'))
                    feat['endings'] += len([e for e in el.findall('ending') if e.get('type') == 'start'])
                    feat['segno'] += len(el.findall('segno'))
                    feat['coda'] += len(el.findall('coda'))
                elif tag == 'sound':
                    for a in ('dacapo', 'dalsegno', 'fine', 'tocoda'):
                        if el.get(a) is not None:
                            feat[a] += 1
                elif tag == 'note':
                    is_chord = el.find('chord') is not None
                    grace = el.find('grace') is not None
                    dur_el = el.find('duration')
                    dur = Fraction(int(float(dur_el.text)), div) if dur_el is not None else Fraction(0)
                    onset = last_onset if is_chord else t
                    nots = el.find('notations')
                    if nots is not None:
                        feat['fingering'] += len(list(nots.iter('fingering')))
                        feat['articulations'] += sum(len(list(a)) for a in nots.findall('articulations'))
                        feat['ornaments'] += sum(len(list(o)) for o in nots.findall('ornaments'))
                        feat['tuplets'] += len([x for x in nots.findall('tuplet') if x.get('type') == 'start'])
                        feat['ties'] += len([x for x in nots.findall('tied') if x.get('type') == 'start'])
                        feat['slurs'] += len([x for x in nots.findall('slur') if x.get('type') == 'start'])
                        feat['fermatas'] += len(nots.findall('fermata'))
                    for ly in el.findall('lyric'):
                        txt = ''.join(x.text or '' for x in ly.findall('text'))
                        if txt.strip():
                            feat['lyrics'] += 1
                            lyrics_by_verse.setdefault(ly.get('number') or ly.get('name') or '1', []).append(txt.strip())
                    p = el.find('pitch')
                    if grace:
                        feat['grace'] += 1
                    elif p is not None:
                        midi = 12 * (int(p.findtext('octave')) + 1) + STEP[p.findtext('step')] + int(round(float(p.findtext('alter') or 0)))
                        staff = f"{pi}.{el.findtext('staff') or '1'}"
                        evs.append((onset, midi, dur, staff))
                        if nots is not None:
                            for fg in nots.iter('fingering'):
                                if (fg.text or '').strip():
                                    fingers.append((mi, onset, midi, fg.text.strip()))
                    if not is_chord and not grace:
                        last_onset = t
                        t += dur
                        mlen = max(mlen, t)
            lengths[mi] = max(lengths.get(mi, 0), mlen)
    ms = [sorted(measures[i]) for i in sorted(measures)]
    for w in words:
        lw = w.lower()
        if re.search(r'\bd\.?\s*c\.?\b|da capo', lw): feat['dacapo'] = max(feat['dacapo'], 1)
        if re.search(r'\bd\.?\s*s\.?\b|dal segno', lw): feat['dalsegno'] = max(feat['dalsegno'], 1)
        if 'to coda' in lw: feat['tocoda'] = max(feat['tocoda'], 1)
        if re.fullmatch(r'fine\.?', lw): feat['fine'] = max(feat['fine'], 1)
    return {
        'parts': len(parts), 'measures': len(ms), 'notes': sum(len(m) for m in ms), 'features': feat,
        'measure_events': ms, 'lengths': [lengths[i] for i in sorted(measures)], 'nominal': [nominal[i] for i in sorted(measures)], 'fingers': fingers, 'harmonies': harmonies, 'lyrics': lyrics_by_verse, 'words': words,
    }


def norm_kind(k):
    k = k.strip().lower()
    return {'major': '', 'minor': 'm', 'dominant': '7', 'dominant-seventh': '7', 'major-seventh': 'maj7', 'minor-seventh': 'm7'}.get(k, k)


def mkey(m, with_staff=False):
    """A measure as a comparable value: onsets, pitches and durations (staff optional)."""
    return tuple((o, p, d, s) if with_staff else (o, p, d) for o, p, d, s in m)


def lcs(a, b):
    if not a or not b:
        return 0
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b):
            cur.append(prev[j] + 1 if x == y else max(prev[j + 1], cur[j]))
        prev = cur
    return prev[-1]


def f1(match, n_pred, n_true):
    if n_pred == 0 or n_true == 0:
        return 0.0
    p, r = match / n_pred, match / n_true
    return 0.0 if p + r == 0 else 2 * p * r / (p + r)


def measure_match(pred, true):
    """Measures of `true` reproduced exactly, after aligning the two measure lists (LCS over whole measures)."""
    return lcs([mkey(m) for m in pred], [mkey(m) for m in true])


def flat(ms, fn):
    return [fn(o, p, d) for m in ms for (o, p, d, s) in m]


def score_against_key(pred, key):
    km, pm = key['measure_events'], pred['measure_events']
    n_true, n_pred = key['notes'], pred['notes']
    pitch = lcs(flat(pm, lambda o, p, d: p), flat(km, lambda o, p, d: p))
    full = lcs(flat(pm, lambda o, p, d: (p, d)), flat(km, lambda o, p, d: (p, d)))
    exact = measure_match(pm, km)
    out = {
        'measures_exact': exact, 'measures_key': len(km), 'measures_clean': exact / len(km),
        'pitch_f1': f1(pitch, n_pred, n_true), 'note_f1': f1(full, n_pred, n_true),
    }
    kh = [h[1:] for h in key['harmonies']]
    ph = [h[1:] for h in pred['harmonies']]
    if kh:
        out['chords_f1'] = f1(lcs(ph, kh), len(ph), len(kh))
    if key['lyrics']:
        norm = lambda s: re.sub(r"[^a-z']", '', s.lower())
        verses = {}
        for kv, ktext in key['lyrics'].items():
            kt = [norm(x) for x in ktext]
            best = 0.0
            for pv, ptext in pred['lyrics'].items():
                pt = [norm(x) for x in ptext]
                best = max(best, f1(lcs(pt, kt), len(pt), len(kt)))
            verses[kv] = best
        out['lyrics_f1_by_verse'] = verses
        out['lyrics_f1'] = sum(verses.values()) / len(verses)
    marks = ['segno', 'coda', 'tocoda', 'dalsegno']
    out['jumps_kept'] = sum(1 for k in marks if pred['features'][k] > 0)
    out['jumps_key'] = len(marks)
    return out


def main():
    tools = sorted(d for d in os.listdir(RES) if os.path.isdir(os.path.join(RES, d)))
    runs = list(csv.DictReader(open(os.path.join(RES, 'runs.csv'))))
    exports = {}
    for t in tools:
        for f in os.listdir(os.path.join(RES, t)):
            m = re.match(r'^([A-J][23]?|X)-', f)
            if m and re.search(r'\.(xml|musicxml|mxl)$', f) and 'separate' not in f:
                exports[(t, m.group(1))] = os.path.join(RES, t, f)
    parsed = {}
    for k, p in sorted(exports.items()):
        try:
            parsed[k] = parse(p)
        except Exception as e:  # noqa: BLE001
            print(f'parse failed: {k} {p}: {e}', file=sys.stderr)

    key_i = parse(os.path.join(HERE, 'keys', 'shenandoah-lead-sheet.musicxml'))
    report = {'tools': tools, 'ids': IDS, 'exports': {}, 'i_scores': {}, 'stability': {}, 'agreement': {}, 'missing': [], 'runs': {}}
    for t in tools:
        for i in IDS:
            if (t, i) not in parsed:
                report['missing'].append(f'{t}/{i}')
    for (t, i), r in parsed.items():
        report['exports'][f'{t}/{i}'] = {'parts': r['parts'], 'measures': r['measures'], 'notes': r['notes'], 'features': r['features'],
                                         'lyric_verses': {v: len(x) for v, x in r['lyrics'].items()}}
    for t in tools:
        if (t, 'I') in parsed:
            report['i_scores'][t] = score_against_key(parsed[(t, 'I')], key_i)
    for t in tools:
        st = {}
        for base, vs in VARIANTS.items():
            if (t, base) not in parsed:
                continue
            b = parsed[(t, base)]['measure_events']
            for v in vs:
                if (t, v) in parsed:
                    st[v] = measure_match(parsed[(t, v)]['measure_events'], b) / max(1, len(b))
        report['stability'][t] = st
    scans = [i for i in IDS if len(i) == 1 and i not in ('X', 'I')]
    for a, b in combinations(tools, 2):
        vals = []
        for i in scans:
            if (a, i) in parsed and (b, i) in parsed:
                ma, mb = parsed[(a, i)]['measure_events'], parsed[(b, i)]['measure_events']
                vals.append(2 * measure_match(ma, mb) / max(1, len(ma) + len(mb)))
        report['agreement'][f'{a}|{b}'] = sum(vals) / len(vals) if vals else None
    for r in runs:
        report['runs'][f"{r['tool']}/{r['id']}"] = {k: r[k] for k in ('outcome', 'seconds', 'cost', 'help_needed', 'warning', 'x_result', 'fingering_shown', 'lyrics_shown', 'chords_shown', 'play_order', 'decoys_ignored', 'fix_minutes')}
    json.dump(report, open(os.path.join(RES, 'analysis.json'), 'w'), indent=1, default=str)
    print(json.dumps({'missing': report['missing'], 'i_scores': report['i_scores'], 'stability': report['stability'], 'agreement': report['agreement']}, indent=1, default=str))


if __name__ == '__main__':
    main()
