"""Rewrite MusicXML so each chord's notes are in ascending pitch (MuseScore canonical order). Nothing else changes."""
import sys, xml.etree.ElementTree as ET
STEP = {'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def key(n):
    p = n.find('pitch')
    if p is None: return -999
    return int(p.findtext('octave'))*12 + STEP[p.findtext('step')] + float(p.findtext('alter') or 0)
src, dst = sys.argv[1:]
tree = ET.parse(src)
for m in tree.iter('measure'):
    kids = list(m); i = 0
    while i < len(kids):
        if kids[i].tag == 'note' and kids[i].find('chord') is None:
            j = i + 1
            while j < len(kids) and kids[j].tag == 'note' and kids[j].find('chord') is not None: j += 1
            group = kids[i:j]
            if len(group) > 1:
                for n in group:
                    c = n.find('chord')
                    if c is not None: n.remove(c)
                group.sort(key=key)
                for n in group[1:]: n.insert(0, ET.Element('chord'))
                for k, n in enumerate(group): m.remove(n)
                for k, n in enumerate(group): m.insert(i + k, n)
                kids = list(m)
            i = j
        else: i += 1
tree.write(dst, encoding='unicode')
