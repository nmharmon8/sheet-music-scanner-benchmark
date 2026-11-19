"""
Scores every tool's export in results/ against the answer keys in keys/ and writes results/scores.json and
results/scores.csv, and prints the summary.

Both sides go through the same normalisation before measures are compared:
- a partial measure is merged with the following measure while the two together fit in one bar (a key writes a
  repeat that falls mid-bar as two measures; many tools write one);
- a first measure that is still short (a pickup) is right-aligned, so a pickup written short and one padded with
  rests compare equal;
- the same pitch starting at the same moment counts once, held for its longest length (a notehead shared by two
  voices, written once by some tools and twice by others, is one key pressed).

Scores (all 0-1):
- measures_clean: key measures reproduced exactly (pitches, onsets and lengths), after aligning the two measure lists.
- note_f1 / pitch_f1: notes matched in order (pitch + length / pitch only), F1 over all notes.
- fingering_f1: (pitch, finger) pairs matched in order; on pages whose key has fingering.
- lyrics_f1: syllables matched in order per key verse, against the tool's best-matching verse; mean over verses.
- chords_f1: chord symbols matched in order (I only).
- repeats: repeat signs and ending brackets kept, against the key's count (capped at 1). jumps: I's four jump marks.
A missing export scores 0 everywhere. X (the blurred photo) is not scored: a reader should always do its best, and
scoring refusals rewarded giving up (dropped 2026-11-17).

    python3 -I score.py
"""
import csv, json, os, re, sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyze as A  # noqa: E402

RES = os.path.join(HERE, 'results')
KX = os.path.join(HERE, 'keys', 'musicxml')
INDEX = json.load(open(os.path.join(HERE, 'index.json')))
UPLOADS = {u['id']: u for u in INDEX['uploads'] if u['id'] != 'X'}
BASE = {u['id']: u.get('variantOf', u['id']) for u in INDEX['uploads']}
GROUPS = {'scan': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'], 'good photo': ['A2', 'C2', 'G2'], 'bad photo': ['A3', 'C3', 'G3'], 'low-res': ['D2']}


def kx(name):
    return A.parse(os.path.join(KX, name + '.musicxml'))


def seq(parts):
    """Pages one after another (F; G with the previous hymn first)."""
    out = {'measure_events': [], 'lengths': [], 'nominal': [], 'fingers': [], 'harmonies': [], 'lyrics': {}, 'features': {}, 'notes': 0}
    for p in parts:
        off = len(out['measure_events'])
        out['measure_events'] += p['measure_events']; out['lengths'] += p['lengths']; out['nominal'] += p['nominal']
        out['fingers'] += [(m + off, o, q, f) for m, o, q, f in p['fingers']]
        out['harmonies'] += [(m + off,) + h[1:] for h in p['harmonies']]
        for v, t in p['lyrics'].items():
            out['lyrics'].setdefault(v, []).extend(t)
        for k, v in p['features'].items():
            out['features'][k] = out['features'].get(k, 0) + v
        out['notes'] += p['notes']
    return out


def stack(parts):
    """Staves of one system kept in separate files (H: piano and voice), merged measure by measure."""
    n = max(len(p['measure_events']) for p in parts)
    out = seq([parts[0]])
    for p in parts[1:]:
        for i in range(n):
            if i < len(p['measure_events']):
                out['measure_events'][i] = sorted(out['measure_events'][i] + p['measure_events'][i])
                out['lengths'][i] = max(out['lengths'][i], p['lengths'][i])
        out['fingers'] += p['fingers']; out['harmonies'] += p['harmonies']
        for v, t in p['lyrics'].items():
            out['lyrics'].setdefault(v, []).extend(t)
        for k, v in p['features'].items():
            out['features'][k] = out['features'].get(k, 0) + v
        out['notes'] += p['notes']
    return out


def keys_for(base):
    """Candidate keys for an upload (the better-scoring one counts)."""
    if base == 'F':
        return {'F': seq([kx('F-beethoven-fur-elise-p1'), kx('F-beethoven-fur-elise-p2'), kx('F-beethoven-fur-elise-p3')])}
    if base == 'G':
        main, prev = kx('G-hymn-gracious-saviour'), kx('G-previous-hymn-daylight')
        return {'hymn only': seq([main]), 'with previous hymn': seq([prev, main])}
    if base == 'H':
        return {'H': stack([kx('H-foster-beautiful-dreamer-piano'), kx('H-foster-beautiful-dreamer-voice')])}
    if base == 'I':
        return {'I': A.parse(os.path.join(HERE, 'keys', 'shenandoah-lead-sheet.musicxml'))}
    names = {'A': 'A-kuhlau-sonatina-op20-1', 'B': 'B-schumann-merry-peasant', 'C': 'C-joplin-entertainer', 'D': 'D-mozart-k545', 'E': 'E-chopin-prelude-20', 'J': 'J-beethoven-minuet-g'}
    return {base: kx(names[base])}


def normalize(p):
    ms, L, N = p['measure_events'], p['lengths'], p['nominal']
    out, i, n = [], 0, len(ms)
    while i < n:
        cur, clen, nom = [(o, q, d) for o, q, d, s in ms[i]], L[i], N[i] or Fraction(4)
        while clen < nom and i + 1 < n and clen + L[i + 1] <= nom and L[i + 1] > 0:
            cur += [(o + clen, q, d) for o, q, d, s in ms[i + 1]]
            clen += L[i + 1]
            i += 1
        if not out and 0 < clen < nom:
            cur = [(o + nom - clen, q, d) for o, q, d in cur]
        held = {}
        for o, q, d in cur:  # one key pressed once: the same pitch at the same onset counts once, held for its longest length
            held[(o, q)] = max(held.get((o, q), d), d)
        out.append(tuple(sorted((o, q, d) for (o, q), d in held.items())))
        i += 1
    return out


def lcs_len(a, b):
    return A.lcs(a, b)


def f1(m, a, b):
    return A.f1(m, a, b)


def norm_text(s):
    return re.sub(r"[^a-z']", '', s.lower().replace('’', "'"))


def digits(f):
    return re.sub(r'\D', '', f)


def score(pred, key):
    pk, kk = normalize(pred), normalize(key)
    out = {'measures_key': len(kk), 'measures_pred': len(pk)}
    out['measures_clean'] = lcs_len(pk, kk) / len(kk) if kk else 0
    fp = [(q, d) for m in pk for o, q, d in m]; fk = [(q, d) for m in kk for o, q, d in m]
    out['note_f1'] = f1(lcs_len(fp, fk), len(fp), len(fk))
    out['pitch_f1'] = f1(lcs_len([q for q, d in fp], [q for q, d in fk]), len(fp), len(fk))
    if key['fingers']:
        a = [(q, digits(f)) for m, o, q, f in sorted(pred['fingers'])]; b = [(q, digits(f)) for m, o, q, f in sorted(key['fingers'])]
        out['fingering_f1'] = f1(lcs_len(a, b), len(a), len(b))
    if key['lyrics']:
        vals = []
        for kv, kt in key['lyrics'].items():
            kt = [norm_text(x) for x in kt]
            vals.append(max([f1(lcs_len([norm_text(x) for x in pt], kt), len(pt), len(kt)) for pt in pred['lyrics'].values()] or [0]))
        out['lyrics_f1'] = sum(vals) / len(vals)
    if key['harmonies']:
        a = [h[1:] for h in pred['harmonies']]; b = [h[1:] for h in key['harmonies']]
        out['chords_f1'] = f1(lcs_len(a, b), len(a), len(b))
    kr = key['features']['repeats'] + key['features']['endings']
    if kr:
        out['repeats'] = min(1, (pred['features']['repeats'] + pred['features']['endings']) / kr)
    jk = sum(1 for k in ('segno', 'coda', 'tocoda', 'dalsegno') if key['features'][k])
    if jk:
        out['jumps'] = sum(1 for k in ('segno', 'coda', 'tocoda', 'dalsegno') if pred['features'][k]) / jk
    return out


def exports():
    found = {}
    for t in sorted(os.listdir(RES)):
        d = os.path.join(RES, t)
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            m = re.match(r'^([A-J][23]?|X)-', f)
            if m and re.search(r'\.(xml|musicxml|mxl)$', f) and 'separate' not in f:
                found[(t, m.group(1))] = os.path.join(d, f)
    return found


def main():
    ex = exports()
    tools = sorted({t for t, _ in ex}, key=lambda t: (t != 'PlayableNotes', t.lower()))
    keycache = {}
    rows, per = [], {}
    for t in tools:
        for uid in UPLOADS:
            base = BASE[uid]
            if base not in keycache:
                keycache[base] = keys_for(base)
            if (t, uid) not in ex:
                r = {'tool': t, 'id': uid, 'missing': True, 'measures_clean': 0, 'note_f1': 0, 'pitch_f1': 0}
                k = next(iter(keycache[base].values()))
                if k['fingers']: r['fingering_f1'] = 0
                if k['lyrics']: r['lyrics_f1'] = 0
                if k['harmonies']: r['chords_f1'] = 0
                rows.append(r)
                continue
            pred = A.parse(ex[(t, uid)])
            best = None
            for kname, k in keycache[base].items():
                s = score(pred, k)
                s['key'] = kname
                if best is None or s['measures_clean'] + s['note_f1'] > best['measures_clean'] + best['note_f1']:
                    best = s
            rows.append({'tool': t, 'id': uid, **best})
            print(f"{t:18} {uid:3} clean {best['measures_clean']:.2f} notes {best['note_f1']:.2f}" + ''.join(f" {k} {best[k]:.2f}" for k in ('fingering_f1', 'lyrics_f1', 'chords_f1', 'repeats', 'jumps') if k in best), file=sys.stderr)

    def mean(t, metric, ids):
        v = [r[metric] for r in rows if r['tool'] == t and r['id'] in ids and metric in r]
        return sum(v) / len(v) if v else None

    allids = list(UPLOADS)
    summary = {}
    for t in tools:
        s = {'measures_clean': mean(t, 'measures_clean', allids), 'note_f1': mean(t, 'note_f1', allids)}
        for g, ids in GROUPS.items():
            s[f'measures_clean {g}'] = mean(t, 'measures_clean', ids)
            s[f'note_f1 {g}'] = mean(t, 'note_f1', ids)
        for m in ('fingering_f1', 'lyrics_f1', 'chords_f1', 'repeats', 'jumps'):
            s[m] = mean(t, m, allids)
        s['missing'] = [r['id'] for r in rows if r['tool'] == t and r.get('missing')]
        summary[t] = s
    json.dump({'tools': tools, 'summary': summary, 'rows': rows}, open(os.path.join(RES, 'scores.json'), 'w'), indent=1, default=str)
    cols = ['tool', 'id', 'key', 'measures_key', 'measures_pred', 'measures_clean', 'note_f1', 'pitch_f1', 'fingering_f1', 'lyrics_f1', 'chords_f1', 'repeats', 'jumps', 'missing']
    with open(os.path.join(RES, 'scores.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore')
        w.writeheader()
        for r in rows:
            w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})
    fmt = lambda v: '  -  ' if v is None else f'{v:5.2f}'
    heads = ['measures_clean', 'measures_clean scan', 'measures_clean good photo', 'measures_clean bad photo', 'measures_clean low-res', 'note_f1', 'fingering_f1', 'lyrics_f1', 'chords_f1', 'repeats', 'jumps']
    print(f"{'tool':18}" + ''.join(f'{h.replace("measures_clean", "clean"):>14}' for h in heads) )
    for t in tools:
        print(f'{t:18}' + ''.join(f'{fmt(summary[t][h]):>14}' for h in heads))


if __name__ == '__main__':
    main()
