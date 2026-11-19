"""
How sure is the ranking? Paired bootstraps of the difference between two tools' mean share of bars read exactly right
(10,000 resamples, seeded per pair, so a pair's interval is the same however the script is called):

- by upload: resample the 17 uploads with replacement;
- by piece: resample the 10 pieces (an upload's photos and screenshot go with their scan), since uploads of the same
  piece aren't independent. This is the more cautious interval.

Also: on how many uploads the first tool was better, tied or worse, and the smallest difference with any one upload
left out. These describe sensitivity to this set of pages, not to printed music in general.

    python3 ci.py [ToolA] [ToolB ...]      # default: PlayableNotes against every other tool
"""
import csv, json, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, 'results', 'scores.csv'))))
score = {(r['tool'], r['id']): float(r['measures_clean'] or 0) for r in rows}
ids = list(dict.fromkeys(r['id'] for r in rows if r['tool'] == 'PlayableNotes'))
piece_of = {u['id']: u.get('variantOf', u['id']) for u in json.load(open(os.path.join(HERE, 'index.json')))['uploads']}
pieces = {}
for i in ids:
    pieces.setdefault(piece_of[i], []).append(i)
tools = list(dict.fromkeys(r['tool'] for r in rows))
if any(a in ('-h', '--help') for a in sys.argv[1:]):
    print(__doc__); sys.exit(0)
main = sys.argv[1] if len(sys.argv) > 1 else 'PlayableNotes'
others = sys.argv[2:] or [t for t in tools if t != main and not t.startswith('PlayableNotes')]
mean = lambda t, s: sum(score.get((t, i), 0) for i in s) / len(s)


def interval(t, draw):
    rng = random.Random(f'{main}|{t}|{draw.__name__}')
    d = sorted(mean(main, s) - mean(t, s) for s in (draw(rng) for _ in range(10000)))
    return d[249], d[9749]


def by_upload(rng):
    return [rng.choice(ids) for _ in ids]


def by_piece(rng):
    keys = list(pieces)
    return [i for k in (rng.choice(keys) for _ in keys) for i in pieces[k]]


print(f'{main}: {mean(main, ids):.1%} over {len(ids)} uploads from {len(pieces)} pieces')
for t in others:
    diff = mean(main, ids) - mean(t, ids)
    (ulo, uhi), (plo, phi) = interval(t, by_upload), interval(t, by_piece)
    w = sum(score.get((main, i), 0) > score.get((t, i), 0) + 1e-9 for i in ids)
    l = sum(score.get((main, i), 0) < score.get((t, i), 0) - 1e-9 for i in ids)
    loo = min((mean(main, [j for j in ids if j != i]) - mean(t, [j for j in ids if j != i]), i) for i in ids)
    print(f'{t:20} {mean(t, ids):6.1%}  difference {diff:+6.1%}  95% by upload {ulo:+.1%} to {uhi:+.1%}'
          f'  by piece {plo:+.1%} to {phi:+.1%}  better/tied/worse {w}/{len(ids) - w - l}/{l}'
          f'  smallest with one upload left out {loo[0]:+.1%} (without {loo[1]})')
