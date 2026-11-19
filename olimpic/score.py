"""
Scores a run (runs/<label>/) with the OLiMPiC authors' own code: our MusicXML's piano part goes through their
Linearizer to LMX, then their TEDn_lmx_xml against the gold MusicXML, flavours "full" and "lmx", summed over systems
as their zeus/tedn_metric.py does (total edit cost / total gold cost). SER is the token edit distance from the gold
LMX over its length. A system with no prediction (a failed run) scores as empty output, as their scorer does.

    olimpic/.venv/bin/python -I olimpic/score.py <label> [--workers 40] [--cached]

Each system is scored from its prediction.musicxml and the result written to runs/<label>/<id>/tedn.json (TEDn is
slow: seconds to minutes a system). --cached reuses the tedn.json files already there instead of scoring again.
"""
import io, json, multiprocessing, os, statistics, sys, time
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'vendor', 'olimpic-icdar24'))
from app.linearization.Linearizer import Linearizer  # noqa: E402
from app.evaluation.TEDn_lmx_xml import TEDn_lmx_xml  # noqa: E402
import Levenshtein  # noqa: E402

DATA = os.path.join(HERE, 'data', 'olimpic-1.0-scanned')
SCORER = 1  # bump when the scoring below changes, so cached tedn.json files are scored again


def piano_part(root):
    """The part with two staves (our export puts any staff above the piano in parts of its own), else the last."""
    parts = root.findall('part')
    for p in parts:
        if any(s.text and s.text.strip() == '2' for s in p.iter('staves')):
            return p
    return parts[-1] if parts else None


def linearize(xml_text):
    errout = io.StringIO()
    if not xml_text:
        return '', 'no prediction'
    try:
        part = piano_part(ET.fromstring(xml_text))
        if part is None:
            return '', 'no part'
        lin = Linearizer(errout=errout, fail_on_unknown_tokens=False)
        lin.process_part(part)
        return ' '.join(lin.output_tokens), errout.getvalue()
    except Exception as e:  # a linearizer crash scores as empty output
        return '', f'linearizer: {e!r}'


def score_one(job):
    run_dir, sid = job
    out = os.path.join(run_dir, sid, 'tedn.json')
    if '--cached' in sys.argv and os.path.exists(out):
        cached = json.load(open(out))
        if cached.get('scorer') == SCORER:
            return cached
    t0 = time.time()
    pred_file = os.path.join(run_dir, sid, 'prediction.musicxml')
    pred_xml = open(pred_file).read() if os.path.exists(pred_file) else ''
    lmx, warnings = linearize(pred_xml)
    gold_xml = open(os.path.join(DATA, sid + '.musicxml')).read()
    gold_lmx = open(os.path.join(DATA, sid + '.lmx')).read().split()
    r = {'id': sid, 'scorer': SCORER, 'predicted': bool(pred_xml), 'predLmx': lmx, 'linearizer_warnings': warnings[:2000],
         'ser_edits': Levenshtein.distance(lmx.split(), gold_lmx), 'ser_gold': len(gold_lmx)}
    for flavor in ('full', 'lmx'):
        t = TEDn_lmx_xml(lmx, gold_xml, flavor=flavor)
        r[flavor] = {'edit': t.edit_cost, 'gold': t.gold_cost}
    r['seconds'] = round(time.time() - t0, 1)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(r, open(out, 'w'), indent=1)
    return r


def main():
    args = sys.argv[1:]
    record = '--record' in args
    workers = int(args[args.index('--workers') + 1]) if '--workers' in args else max(1, (os.cpu_count() or 2) - 8)
    label = [a for i, a in enumerate(args) if not a.startswith('--') and (i == 0 or args[i - 1] != '--workers')][0]
    run_dir = os.path.join(HERE, 'runs', label)
    meta = json.load(open(os.path.join(run_dir, 'run.json')))
    ids = meta['ids']
    rows = []
    with multiprocessing.Pool(workers) as pool:
        # longest first, as the authors' script does, so one slow system doesn't finish last alone
        order = sorted(ids, key=lambda s: -os.path.getsize(os.path.join(DATA, s + '.lmx')))
        for n, r in enumerate(pool.imap_unordered(score_one, [(run_dir, s) for s in order]), 1):
            rows.append(r)
            print(f'scored {n}/{len(ids)}', end='\r', file=sys.stderr)
    print(file=sys.stderr)
    results = {}
    for s in ids:
        f = os.path.join(run_dir, s, 'result.json')
        results[s] = json.load(open(f)) if os.path.exists(f) else {}

    pct = lambda a, b: 100 * a / b if b else 0.0
    tot = lambda k, f: sum(r[f][k] for r in rows)
    full = pct(tot('edit', 'full'), tot('gold', 'full'))
    lmx = pct(tot('edit', 'lmx'), tot('gold', 'lmx'))
    ser = pct(sum(r['ser_edits'] for r in rows), sum(r['ser_gold'] for r in rows))
    failed = [s for s in ids if not results[s].get('ok')]
    secs = [results[s]['seconds'] for s in ids if 'seconds' in results[s]]
    songs = len({s.split('/')[1] for s in ids})
    summary = {'label': label, **{k: meta[k] for k in ('date', 'commit', 'sample')},
               'systems': len(ids), 'songs': songs, 'tednFull': round(full, 2), 'tednLmx': round(lmx, 2), 'ser': round(ser, 2),
               'failed': len(failed), 'medianSeconds': statistics.median(secs) if secs else None}
    json.dump({**summary, 'perSystem': sorted(({'id': r['id'], 'full': pct(r['full']['edit'], r['full']['gold']),
               'lmx': pct(r['lmx']['edit'], r['lmx']['gold']), 'ser': pct(r['ser_edits'], r['ser_gold'])} for r in rows),
               key=lambda x: -x['full'])}, open(os.path.join(run_dir, 'summary.json'), 'w'), indent=1)
    worst = sorted(rows, key=lambda r: -pct(r['full']['edit'], r['full']['gold']))[:10]
    md = [f'# OLiMPiC scanned test · {label}', '',
          f'{len(ids)} systems from {songs} songs ({meta["sample"]}) · commit {meta["commit"][:8]}', '',
          '| metric | ours | Zeus (paper, scanned, augmented) |', '|---|---:|---:|',
          f'| TEDn full (lower is better) | {full:.2f}% | 18.40% |',
          f'| TEDn lmx | {lmx:.2f}% | 14.85% |',
          f'| SER | {ser:.2f}% | 17.72% |', '',
          f'Failed runs (scored as empty output): {len(failed)} · '
          f'median {summary["medianSeconds"]} s a system', '', '## Worst ten systems (TEDn full)', '']
    md += [f'- `{r["id"]}`: {pct(r["full"]["edit"], r["full"]["gold"]):.2f}%' for r in worst]
    open(os.path.join(run_dir, 'summary.md'), 'w').write('\n'.join(md) + '\n')
    print('\n'.join(md))

    if record:
        path = os.path.join(HERE, 'results.md')
        music_file = os.path.join(run_dir, 'music.json')
        music = json.load(open(music_file)) if os.path.exists(music_file) else {}
        notes = f"{music['noteErrorRate']:.2f}%" if music else '–'
        line = (f'| {meta["date"][:10]} | {label} | {meta["commit"][:8]} | {meta["sample"]} ({len(ids)}) '
                f'| {notes} | {full:.2f}% | {lmx:.2f}% | {ser:.2f}% | {len(failed)} |')
        lines = open(path).read().rstrip('\n').split('\n')
        lines = [l for l in lines if f'| {label} |' not in l] + [line]
        open(path, 'w').write('\n'.join(lines) + '\n')
        print(f'recorded in {path}')


if __name__ == '__main__':
    main()
