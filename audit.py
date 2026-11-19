"""
Key audit: could a wrong answer key be favouring PlayableNotes (whose maker wrote the keys)? Lists every key bar that
PlayableNotes matched while at least three other tools read the same bar identically to each other and differently
from the key. Those are the bars where the key, not the other tools, would most likely be wrong. Each is to be checked
by eye against the source image in keys/src/ (verdicts in keys/AUDIT.md).

Bars are aligned as the scorer does (in order, whole bars, after its normalisation); an unmatched key bar is compared
with the export bar in the same position of the gap. The hymn (G) is audited on its 16-bar key for every tool.

    python3 audit.py
"""
import os, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score as S  # noqa: E402
from diffbars import show  # noqa: E402

OTHERS = ['Soundslice', 'Songscription', 'Halbestunde', 'Scan2Notes', 'Playscore2', 'SheetMusicScanner']


def align(kk, pk):
    """Key bar index -> the tool's bar there: its match, or the bar in the same position of the unmatched gap."""
    n, m = len(kk), len(pk)
    L = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            L[i][j] = L[i + 1][j + 1] + 1 if kk[i] == pk[j] else max(L[i + 1][j], L[i][j + 1])
    i = j = 0; matched = {}
    while i < n and j < m:
        if kk[i] == pk[j]: matched[i] = j; i += 1; j += 1
        elif L[i + 1][j] >= L[i][j + 1]: i += 1
        else: j += 1
    out = {}
    for i in range(n):
        if i in matched:
            out[i] = (True, pk[matched[i]])
            continue
        # Inside a run of unmatched key bars between two matches, the k-th key bar goes with the k-th export bar of
        # the same gap (not every bar of the run with the gap's first).
        pi = max([k for k in matched if k < i], default=-1)
        jj = matched.get(pi, -1) + 1 + (i - pi - 1)
        nxt = min([matched[k] for k in matched if k > i], default=m)
        out[i] = (False, pk[jj] if jj < nxt else ())
    return out


def main():
    ex = S.exports()
    flagged = 0
    for uid in S.UPLOADS:
        keys = S.keys_for(S.BASE[uid])
        key = keys.get('with previous hymn') or next(iter(keys.values()))
        kk = S.normalize(key)
        al = {t: align(kk, S.normalize(S.A.parse(ex[(t, uid)]))) for t in ['PlayableNotes'] + OTHERS if (t, uid) in ex}
        for i in range(len(kk)):
            if not al['PlayableNotes'][i][0]:
                continue
            wrong = [tuple(al[t][i][1]) for t in OTHERS if t in al and not al[t][i][0] and al[t][i][1]]
            reading, n = Counter(wrong).most_common(1)[0] if wrong else ((), 0)
            if n >= 3:
                flagged += 1
                ks, rs = set(kk[i]), set(reading)
                who = [t for t in OTHERS if t in al and not al[t][i][0] and tuple(al[t][i][1]) == reading]
                print(f'{uid:3} bar {i + 1:3}: {n} other tools agree on another reading ({", ".join(who)})'
                      f'\n      key has   {show(sorted(ks - rs))[:150]}\n      they have {show(sorted(rs - ks))[:150]}')
    print(f'{flagged} key bars to check by eye')


if __name__ == '__main__':
    main()
