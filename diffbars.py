"""
Shows which key measures a tool got wrong on one upload, after the scorer's normalisation:

    python3 -I diffbars.py <Tool> <id> [max]
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score as S  # noqa: E402

NAMES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']


def name(q):
    return f'{NAMES[q % 12]}{q // 12 - 1}'


def show(m):
    return ' '.join(f'{name(q)}@{o}/{d}' for o, q, d in m)


def main():
    tool, uid = sys.argv[1], sys.argv[2]
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    pred = S.A.parse(S.exports()[(tool, uid)])
    keys = S.keys_for(S.BASE[uid])
    # The same choice as score.py: the key giving the higher bars-exact plus note F1.
    kname, key = max(keys.items(), key=lambda kv: (lambda r: r['measures_clean'] + r['note_f1'])(S.score(pred, kv[1])))
    pk, kk = S.normalize(pred), S.normalize(key)
    # LCS alignment over whole measures, then report unmatched key measures with the nearest tool measure.
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
    print(f'{tool} {uid} key={kname}: {len(matched)}/{n} key measures exact; tool has {m} measures')
    shown = 0
    for i in range(n):
        if i in matched: continue
        # The export bar in the same position of the unmatched gap (as audit.py).
        pi = max([k for k in matched if k < i], default=-1)
        jj = matched.get(pi, -1) + 1 + (i - pi - 1)
        nxt = min([matched[k] for k in matched if k > i], default=m)
        cand = pk[jj] if jj < nxt else ()
        ks, ps = set(kk[i]), set(cand)
        print(f'  key M{i + 1}: missing {show(sorted(ks - ps))[:160]}')
        print(f'  {" " * len(str(i + 1))}       extra   {show(sorted(ps - ks))[:160]}')
        shown += 1
        if shown >= limit: break


if __name__ == '__main__':
    main()
