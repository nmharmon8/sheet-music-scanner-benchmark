# Scan2Notes benchmark — 2026-11-16

The user's paid Scan2Notes account was used in Chrome to run all 18 uploads in
`../../index.json`. Each original image or PDF was uploaded as supplied, once, with
**Start full scan** (not demo). The three-page *Für Elise* PDF was one upload. The
site required a title, composer and rights/terms attestation for every run; the
benchmark's source attribution was entered and the user confirmed the attestation
for all 18. No cropping, rotation, staff selection, review choices or edits were
made. The scan detail panels reported `Auto-Detect` for transcription mode,
instruments and key. All 18 finished and offered a MusicXML export.

The account showed **Scan2Notes Pro Yearly**, active, with **32 of 50 subscription
tickets left** after the 18 uploads. Thus each full scan consumed one ticket,
including the three-page PDF. The page displayed a 12/15/2026 ticket reset. The
actual subscription payment was not checked. The upload dialog accepted PDF, JPG
and PNG; the download menu offered MusicXML, PDF, MIDI, LilyPond and GP5. MusicXML
was saved for the benchmark.

## Saved MusicXML

The figures below count elements in the files, **not transcription accuracy**.
`Notes` means pitched notes, excluding rests. Every file parses as MusicXML
`score-partwise`. The filenames start with the upload ID from `../../index.json`.

| Input | Measures | Pitched notes | Parts | File |
|---|---:|---:|---:|---|
| A | 41 | 530 | 1 | `A-kuhlau-sonatina-op20-1.musicxml` |
| B | 21 | 354 | 1 | `B-schumann-merry-peasant.musicxml` |
| C | 16 | 290 | 1 | `C-joplin-entertainer.musicxml` |
| D | 19 | 330 | 1 | `D-mozart-k545.musicxml` |
| E | 21 | 391 | 1 | `E-chopin-prelude-20.musicxml` |
| F | 82 | 656 | 1 | `F-beethoven-fur-elise-full-pdf.musicxml` |
| G | 32 | 254 | 2 | `G-hymn-gracious-saviour.musicxml` |
| H | 36 | 171 | 3 | `H-foster-beautiful-dreamer.musicxml` |
| I | 17 | 44 | 1 | `I-shenandoah-lead-sheet.musicxml` |
| J | 38 | 332 | 1 | `J-beethoven-minuet-g.musicxml` |
| C2 | 16 | 290 | 1 | `C2-joplin-entertainer-photo-good.musicxml` |
| C3 | 16 | 290 | 1 | `C3-joplin-entertainer-photo-bad.musicxml` |
| G2 | 32 | 254 | 2 | `G2-hymn-gracious-saviour-photo-good.musicxml` |
| G3 | 32 | 248 | 2 | `G3-hymn-gracious-saviour-photo-bad.musicxml` |
| A2 | 41 | 536 | 1 | `A2-kuhlau-sonatina-photo-good.musicxml` |
| A3 | 41 | 533 | 1 | `A3-kuhlau-sonatina-photo-bad.musicxml` |
| D2 | 19 | 328 | 1 | `D2-mozart-k545-screenshot-lowres.musicxml` |
| X | 300 | 0 | 1 | `X-unreadable-photo.musicxml` |

Across **all 18 exports**, the standard MusicXML counts are zero for fingering,
lyrics, chord symbols (`<harmony>`), repeats, endings, pedal, articulations and
dynamics. The source images include printed examples of these features, especially
fingering on A/B/D/E/F, lyrics on G/H/I, and chords on I. This establishes what
the **exports** retain; the app's on-screen rendering was not separately graded.
Key, time, clef and pitched-note elements are present on legible uploads.

F's export has 82 measure elements and 656 pitched notes after the complete
three-page PDF upload. This count alone cannot establish whether every page and
staff was captured; its eventual answer-key comparison must decide that.

## Unreadable control and timing

X did **not** show a refusal or low-confidence warning in the observed scan and
songbook flow. It completed and exported 300 measures, each with a whole-measure
rest, and **zero pitched notes**. This is an unusable, empty result; it is not
invented playable notes. The title and composer entered for this upload identified
the underlying public-domain Chopin source, a possible contextual cue. X has no
readable note-level ground truth and is excluded from note-accuracy denominators.

Scans ran concurrently in the songbook. A completed within roughly 42 seconds of
pressing **Start full scan**; other completions were not timed consistently.
`seconds` is therefore blank in `../runs.csv` rather than presenting noncomparable
processing observations as upload-to-playable measurements. No per-run warning was
observed. The optional playback checks and 15-minute correction exercises in the
rubric were not performed; blank fields in the run log mean unmeasured.

Objective note and measure accuracy still requires the source answer keys for
A–H and J. The key for I exists at `../../keys/shenandoah-lead-sheet.musicxml`.
