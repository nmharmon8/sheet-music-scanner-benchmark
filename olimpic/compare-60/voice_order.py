"""Re-serialize MusicXML measures voice by voice (MuseScore's canonical order): attributes, then each (staff, voice)'s
notes in time order with <forward> for gaps and <backup> between voices; directions kept before the first voice at their
onset. Pitches, durations, chords, beams, ties and notations are untouched. args: src dst"""
import sys, copy, xml.etree.ElementTree as ET
src, dst = sys.argv[1:]
tree = ET.parse(src)
def dur(e):
    d = e.find('duration'); return int(float(d.text)) if d is not None and d.text else 0
for m in tree.iter('measure'):
    pos = 0; last_onset = 0; head = []; tail = []; events = []; dirs = []; mlen = 0
    for e in list(m):
        if e.tag == 'note':
            if e.find('chord') is not None:
                events[-1][2].append(e); continue
            v = (int(e.findtext('staff') or 1), int(e.findtext('voice') or 1))
            events.append([v, pos, [e]]); last_onset = pos
            if e.find('grace') is None: pos += dur(e)
        elif e.tag == 'backup': pos -= dur(e)
        elif e.tag == 'forward': pos += dur(e)
        elif e.tag == 'attributes' and not events: head.append(e)
        elif e.tag == 'barline': tail.append(e)
        elif e.tag in ('direction', 'harmony', 'attributes', 'sound', 'print'): dirs.append((pos, e))
        else: dirs.append((pos, e))
        mlen = max(mlen, pos)
    if not events: continue
    for e in list(m): m.remove(e)
    for e in head: m.append(e)
    voices = sorted({v for v, _, _ in events}, key=lambda v: (v[1], v[0]))
    cur = 0; first = True
    for v in voices:
        if not first and cur > 0:
            b = ET.SubElement(m, 'backup'); ET.SubElement(b, 'duration').text = str(cur); cur = 0
        evs = sorted([x for x in events if x[0] == v], key=lambda x: x[1])
        pend = sorted(dirs, key=lambda d: d[0]) if first else []
        for _, onset, group in evs:
            while pend and pend[0][0] <= onset:
                p, d = pend.pop(0)
                if p > cur:
                    f = ET.SubElement(m, 'forward'); ET.SubElement(f, 'duration').text = str(p - cur); cur = p
                m.append(d)
            if onset > cur:
                f = ET.SubElement(m, 'forward'); ET.SubElement(f, 'duration').text = str(onset - cur); cur = onset
            for n in group: m.append(n)
            if group[0].find('grace') is None: cur = max(cur, onset + dur(group[0]))
        for _, d in pend: m.append(d)
        first = False
    for e in tail: m.append(e)
tree.write(dst, encoding='unicode')
