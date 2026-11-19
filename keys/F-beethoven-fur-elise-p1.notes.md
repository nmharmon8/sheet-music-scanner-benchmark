# F p1: Beethoven, Für Elise (Wier 1913, p. 13)

- 6 systems, 37 measures: S1 M1-M7 (M1 = one-eighth pickup), S2 M8-M14, S3 M15-M21, S4 M22-M27, S5 M28-M33,
  S6 M34-M37. Endings: M9 `[1` (two eighths long) `:|`, M10 `[2`; M11 `|:`; M24 `[1` `:|`, M25 `[2`.
  Clefs: LH to treble mid-M14, back to bass at the end of M17 (after the whole rest).
- **Continues onto page 2:** the RH slur that starts on M37's first E5 ends on page 2's first note (E5). No ties on the page.
  Two beams cross a barline, which the key doesn't record: LH E4 (M14) to E5 (M15), RH D#5 (M15) to E5 (M16).

## Printed but not in the key
- Pedal (Ped. then *): M3, M4, M5, M7, M8, M9, M10, M11, M12, M13, M14 (the * comes at M15's second sixteenth),
  M18, M19, M20, M22, M23, M24, M25. No pedal marks in M1-M2, M6, M15-M17, M21 or M26-M37.
- Text: *Poco moto* (M1), *dim.* (M13), *dim. e rit.* (M15-M16), *a tempo* (M17), *dolce* and LH *legato* (M26),
  *cresc.* (M30, followed by a hairpin), *dim.* (M32).
- The ends of slurs inside the second endings: the arc under A4 at the start of M10 (slur from M8's E4) and of M25
  (slur from M23's E4). Also the grace-note slurs in M26 (F4 A4 to C5) and M29 (B4 to A4), which overlap the main
  slurs; the key can't hold one slur inside another.
- M32: the turn is printed after the C5 (a delayed turn, between C5 and D5). It's written as `\turn` on C5.

## Uncertain readings
- M5, M20: the slur starts above E4's stem, before the E5, so it's keyed from E4. M35: the new slur after the one
  ending on C5 starts over the G4 (3rd 32nd) and is keyed there; it could also be read from the G5. M28 and M37: the slur
  starts just to the right of the fingering on the first note, so it's keyed from the first note.
- M2/M6/M17/M21: the < hairpin ends just before the third note, so it's keyed over notes 1-3 and the > over notes 4-6.
- M29: the > is wide (it spans Bb4-A4), so it's a `<dim>` hairpin. The short > marks under F5 (M26) and Bb5 (M27) are accents.
- Fingers joined by a small arc are substitutions: M12 and M13 `3-4`, M30 `4-1`. The M25 LH stack 1-over-2 sits under
  the chord [Bb3 C4], so it's keyed as [2 1].
- M29 grace: a small eighth with a slash on B4 (Bb by the measure's flat), so it's keyed `B4/8gs`.
- M17 LH `{G} R {F}` is the canonical spelling: `formatScore` writes a clef after a full-measure rest this way. The parser
  places it at onset 0, and the render then leaves the bass clef out, so M18 onward draws in treble. The render was
  checked with `r/4.` in its place. This is a renderer quirk, not part of the reading.

## Reference
Mutopia LilyPond was used only as a cross-check, and
the page was followed where it differs: M16 RH E5/16 r/16 r/16 (Mutopia E5/8 r/16); M29 grace as a slashed eighth
(Mutopia a 32nd appoggiatura); M33-M36 LH stay in bass clef with ledger lines (Mutopia changes to treble); Wier's
slurs, hairpins and fingering throughout.
