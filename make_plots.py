"""
Builds results/plots.html from results/scores.json (score.py) and plots.template.html.

    python3 -I score.py && python3 -I make_plots.py
"""
import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, 'results')
s = json.load(open(os.path.join(RES, 'scores.json')))
# The earlier PlayableNotes reading stays in scores.json and the README for comparison; the charts show the current one.
T = [t for t in s['tools'] if not t.startswith('PlayableNotes-')]
cells = {t: {r['id']: r for r in s['rows'] if r['tool'] == t } for t in T}


def mean(t, ids):
    v = [cells[t][i]['measures_clean'] for i in ids if i in cells[t]]
    return sum(v) / len(v) if v else None


quality = {t: {'scan': mean(t, 'ACG'), 'good': mean(t, ['A2', 'C2', 'G2']), 'bad': mean(t, ['A3', 'C3', 'G3']), 'D': mean(t, ['D']), 'D2': mean(t, ['D2'])} for t in T}
runs = list(csv.DictReader(open(os.path.join(RES, 'runs.csv'))))
comp = {}
for t in T:
    rs = [r for r in runs if r['tool'].lower() == t.lower()]
    comp[t] = {'exports': 17 - len(s['summary'][t]['missing']),
               'seconds': sum(1 for r in rs if r['seconds'].strip() and r['id'] != 'X')}
index = json.load(open(os.path.join(HERE, 'index.json')))
names = {u['id']: u.get('title', u.get('slug', '')) for u in index['uploads']}
data = {'tools': T, 'summary': s['summary'], 'cells': cells, 'quality': quality, 'completeness': comp, 'pageNames': names}
html = open(os.path.join(HERE, 'plots.template.html')).read().replace('__DATA__', json.dumps(data, default=str))
open(os.path.join(RES, 'plots.html'), 'w').write(html)
print('results/plots.html')
