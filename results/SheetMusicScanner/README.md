# Sheet Music Scanner export mapping — 2026-11-16

The user ran the mobile app manually and saved the results here. They recall paying about **$19.99 once** for the app and estimate **about 4 seconds per page** to process; neither figure was checked against a receipt or stopwatch. The three-page F PDF would be roughly 12 seconds by that estimate, not a measured run time. All 20
MusicXML files parse. Their internal `work-title` values match the original
benchmark input filenames, and the four `Screenshot_20261116-1328*.png` images
show the corresponding input thumbnails in the app. Those two signals establish
the mapping below. The original filenames are recorded so the renames can be
traced. No two exports are byte-identical or have an identical ordered note
sequence.

| ID | Renamed MusicXML | Original MusicXML filename |
|---|---|---|
| A | `A-kuhlau-sonatina-op20-1.musicxml` | `kuhlau-sonatina-op20-1-schirmer-1893-p1.musicxml` |
| B | `B-schumann-merry-peasant.musicxml` | `schumann-merry-peasant-op68-10-ricordi-1919.musicxml` |
| C | `C-joplin-entertainer.musicxml` | `joplin-entertainer-stark-1902-p1.musicxml` |
| D | `D-mozart-k545.musicxml` | `mozart-k545-i-schirmer-1893-p1.musicxml` |
| E | `E-chopin-prelude-20.musicxml` | `chopin-prelude-op28-20-schirmer-1895.musicxml` |
| F | `F-beethoven-fur-elise-full-pdf.musicxml` | `beethoven-fur-elise-wier-1913.musicxml` |
| G | `G-hymn-gracious-saviour.musicxml` | `hymn-gracious-saviour-new-century-1904.musicxml` |
| H | `H-foster-beautiful-dreamer.musicxml` | `foster-beautiful-dreamer-pond-1864-p1.musicxml` |
| I | `I-shenandoah-lead-sheet.musicxml` | `shenandoah-lead-sheet.musicxml` |
| J | `J-beethoven-minuet-g.musicxml` | `beethoven-minuet-g-woo10-2-breitkopf.musicxml` |
| C2 | `C2-joplin-entertainer-photo-good.musicxml` | `joplin-entertainer-stark-1902-p1-photo-good.musicxml` |
| C3 | `C3-joplin-entertainer-photo-bad.musicxml` | `joplin-entertainer-stark-1902-p1-photo-bad.musicxml` |
| G2 | `G2-hymn-gracious-saviour-photo-good.musicxml` | `hymn-gracious-saviour-new-century-1904-photo-good.musicxml` |
| G3 | `G3-hymn-gracious-saviour-photo-bad.musicxml` | `hymn-gracious-saviour-new-century-1904-photo-bad.musicxml` |
| A2 | `A2-kuhlau-sonatina-photo-good.musicxml` | `kuhlau-sonatina-op20-1-schirmer-1893-p1-photo-good.musicxml` |
| A3 | `A3-kuhlau-sonatina-photo-bad.musicxml` | `kuhlau-sonatina-op20-1-schirmer-1893-p1-photo-bad.musicxml` |
| D2 | `D2-mozart-k545-screenshot-lowres.musicxml` | `mozart-k545-i-schirmer-1893-p1-screenshot-800px.musicxml` |
| X | **No export** | The user reports the app said `no music found`. The X upload is visible in `Screenshot_20261116-132855.png`. |

The three additional files are the individual pages of F, imported separately:
`F-page1-separate.musicxml`, `F-page2-separate.musicxml`, and
`F-page3-separate.musicxml` (originally
`beethoven-fur-elise-wier-1913-p1.musicxml` through `p3.musicxml`). They are
**diagnostic outputs**, not extra benchmark runs or accidental duplicate files.
The complete-PDF F file is the benchmark result. The full export has 849 pitched
notes; the three page exports have 316, 274, and 257 respectively. The slight
difference is consistent with separate recognition runs, so the page files should
not be substituted for the full-PDF result.

The only missing expected MusicXML is X, which is a recorded refusal rather than
an omitted benchmark input. `../runs.csv` now has one Sheet Music Scanner row per
benchmark ID. The user-supplied speed and purchase estimates are recorded above. Per-run
`seconds` remains blank because upload-to-playable intervals were not measured with
a stopwatch; settings and interventions are also unrecorded. No run time should
be inferred from file modification times. The files are ready for later answer-key scoring.
