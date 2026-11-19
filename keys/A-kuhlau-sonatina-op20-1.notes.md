# A: Kuhlau, Sonatina Op. 20 No. 1 i, p. 1 (Schirmer 1893): key notes

**Layout:** 7 systems, 41 measures, all in C major and 4/4. S1 is M1–6, S2 M7–13, S3 M14–19, S4 M20–25, S5 M26–29, S6 M30–35 and S7 M36–41. The end-repeat of the exposition is mid-system, after M31. The page ends inside the development, so M41 continues on page 4.

**Printed but not in the key:**
- Tempo: *Allegro* (M1).
- Words: *legato.* (M2, M18, M33 LH), *dolce.* (M17, M32), *cresc.* (M28, M39) and *dim.* (M30).
- The footnote mark a) under M1–2 LH and the footnote text at the foot of the page.
- The title, credits, copyright line and plate number.
- In M31 a second fingering, 1 4 3, is printed below F5 E5 D5. It is the fingering into M32; the key keeps the one printed above the notes (1 3).
- Slurs the key can't hold: a the key voice line can't have one slur end on the note where another begins. Where that happens, a phrase slur is kept over a connecting slur (the small slurs of footnote a); otherwise the slur that starts on the note is kept. Dropped:
  - LH connecting slurs: M1→M2, M6→M7, M16→M17, M17→M18, M20→M21 and M32→M33.
  - RH slurs: M21 B5→M24 G4 and M28 G4→M30 G6.

**Readings I made:**
- **M1 LH clef:** a bass clef at the system start, then a treble clef before the first note. Written `{F} {G}`; the pitches are read in treble. The MusicXML export draws only the first clef at a point. The MusicXML importer also keeps only the first clef at onset 0, so a tool can match only one of the two clef facts.
- **LH phrase slurs in M1, M17 and M32:** the printed arc ends just before the 8th note, where the connecting slur starts. Written to the 8th note, since the footnote says the phrase slur covers the measure.
- **M7→M8 LH:** two arcs are printed, one above the chord and one below. Written as one slur.
- **M2:** the tied G5 eighth has a staccato dot as printed.
- **Triplets, M13–16:** the tuplet 3 is printed only in M13, beside the fingers 1 2; it is not a finger. M14–16 are unmarked triplets and are written `t3`.
- **Fingers printed on the top staff line, where the glyph is blotted:**
  - M24 C5 and M33 beat-4 C5 are read as 1. A 1 fits the scale fingering in M24 and the M32–34 pattern in M33, and Mutopia has c-1 in M24.
  - M32 B4 is 1.
  - M19 C5 is read as 3 (it might be a 2).
- **M26 and M28 LH:** a single 3 is printed at the stem end of [G3 B3]. It is put on G3, as on the single G3 of M24.
- **Left hand, one voice:** index.json says the LH has two voices. On this page every LH chord is on one stem, so the LH is written as one voice.
- **Dynamics:** the mf in M8, p in M9 and mf in M21 are printed under the rests and are placed on those rests. The sf in M30 is placed in the RH. Hairpin ends are put on the nearest note.
- **Ignored:** a speck under the 7th RH note of M15.

**Reference:** Mutopia 232 was used as a cross-check of notes and rhythm only. Every measure was checked against the page. The page wins where they differ, for example:
- M5 eighth finger 3 (Mutopia has 4).
- M13 RH mf / LH f (Mutopia has f).
- Most fingering, the tenutos and the slurs come from the page only.

**A3 (bad photo):** a sheet of paper in the frame covers the right end of the last system, hiding the LH quarter rest at the end of M41. A reading of A3 that leaves that beat empty (`s/4`) is right for what the photo shows. score.py ignores rests, so the published scores are unaffected; per-bar the key scoring of A3 should treat M41's rest as optional.
