# Key audit

PlayableNotes made these answer keys, so a wrong key could favour it. `python3 audit.py` lists every key bar that
PlayableNotes matched while at least three other tools read that bar identically to each other and differently from
the key: the bars where the key, rather than the other tools, would most likely be wrong.

**Result: 7 bars, none on the ten scans and lead sheet: bars 1, 2, 4 and 6 of A2 (the good photo of the Kuhlau), bars
1 and 2 of A3 (its bad photo) and bar 1 of D2 (the 800-pixel screenshot of the Mozart).** Verdict: the keys are right.

- The three tools are the same in all seven: Halbestunde, Scan2Notes and Sheet Music Scanner. Halbestunde and Scan2Notes
  use the same recognition engine, so their agreement is one reading, not two.
- In every one of these bars they have the key's left-hand notes a sixth lower (C4 as E2, D4 as F2, G4 as B2): the
  left-hand staff read in bass clef where the page prints a treble clef. Both pieces open with the left hand in the
  treble clef.
- On the clean scans of the same pieces, the key's reading is confirmed by other tools: on A, Soundslice matched 8 of
  the first 8 bars exactly, PlayScore 2 7 and Sheet Music Scanner itself 6; on D, Soundslice matched 4 of the first 5.

How the check works: bars are aligned as the scorer does (whole bars, in order, after its normalisation), and an
unmatched key bar is compared with the export bar in the same position of the gap; the hymn (G) is audited on its
16-bar key for every tool. The keys were drafted by Claude Opus 5.5 agents, one per piece (`BRIEF.md`), and checked in verification rounds.
