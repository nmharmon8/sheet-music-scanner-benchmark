# C, joplin-entertainer: notes on the key

- **Layout:** 4 systems of 4 measures each, so 16 measures. M1-M4 are the intro (system 1, which ends with a double bar). M5-M16 are the first strain: a start-repeat at M5, and its end-repeat is on page 2. M16 ends with a plain barline. The key is C major (0) and the time is 2/4 throughout.
- **Printed but not in the key:**
  - The text above the music: page number "2", "Dedicated to James Brown and his Mandolin Club.", the title, "A Rag Time Two Step", "By Scott Joplin".
  - "INTRO:" and the tempo "Not fast." at M1.
  - The copyright line.
  - In M3 the RH 16th group D4 E4 C4 is beamed across to an A3 on the bass staff, and the melody continues there (A3~A3 B3 A3 Ab3, stems up). The key puts those notes on `M3 LH` (voice 1) and gives the RH a spacer, so the cross-staff beam is not recorded.
- **Ledger lines are engraved too far from the staff.** This applies to M1 upper voice, M2 LH, and every ledger note on the page. The ledger lines, and the notes on them, sit about a third to a half space further from the staff than standard. Measured from the staff lines, the M1 upper voice comes out a step high (E6 F6 D6 B5 B5 C6) and so does the start of M2 LH (E4 F4 D4). I read every ledger note by counting ledger lines and checking whether the note is on a line or in a space:
  - M1 upper voice: D6 E6 C6 A5~A5 B5, then G5 (in the space above the staff, no ledger line).
  - M2 LH: D4 E4 C4.
  - M3 RH: C4.
  - G1 in M4, the C6/D6/E6 octave tops, the C4/E4 chord tops and E2/D2 below the bass staff.

  Read this way, the intro is the octave doubling of the lower voice, and Mutopia agrees.
- **Uncertain spots:**
  - M4: the decrescendo hairpin starts between the chord and the D4 16th, a little nearer D4. I put `<dim>` on D4. In M8 and M12 the same hairpin clearly starts at the chord.
  - M4 LH voices: G3/8 r/8 has stems up (LH). G2/8 r/8 has stems down, and [G1 G2]/8-^ [G3 B3]/8 is beamed with stems down, so both are in LH2. The other LH voice has a spacer on beat 2, because no rest is printed there.
  - M12: the natural on F5 is printed as a cautionary natural after M11's F#5, so it is written `Fn5`.
- **Reference edition:** I used the Mutopia LilyPond only as a cross-check. Its pitches, rhythms and ties agree with the page for M1-M16. Where it differs, I followed the page:
  - Mutopia has a slur on D4-D#4 in M4. The page has none there; it has slurs only in M8 and M12.
  - Mutopia has none of the page's hairpins. These are a dim in M4, M8 and M12, and a cresc in M6, M10 and M14. M10's hairpin opens to the right.
