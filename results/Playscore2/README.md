# PlayScore 2 export mapping

The 20 MusicXML files here all parse. Their names start with the benchmark upload ID from `../../index.json`. The mapping uses the music in each export, the app's title-grid screenshots, and the original export timestamps. The app saved 22 items: 18 benchmark inputs, three extra single-page *Für Elise* imports, and one duplicate Chopin import. The redundant Chopin export has been removed.

| Benchmark input | MusicXML export | Original export name |
|---|---|---|
| A — Kuhlau scan | `A-kuhlau-sonatina-op20-1.xml` | `Untitled(15).xml` |
| A2 — Kuhlau good photo | `A2-kuhlau-sonatina-photo-good.xml` | `Untitled(14).xml` |
| A3 — Kuhlau bad photo | `A3-kuhlau-sonatina-photo-bad.xml` | `Untitled(13).xml` |
| B — Schumann | `B-schumann-merry-peasant.xml` | `Untitled(18).xml` |
| C — Joplin scan | `C-joplin-entertainer.xml` | `Untitled(12).xml` |
| C2 — Joplin good photo | `C2-joplin-entertainer-photo-good.xml` | `Untitled(11).xml` |
| C3 — Joplin bad photo | `C3-joplin-entertainer-photo-bad.xml` | `Untitled(10).xml` |
| D — Mozart scan | `D-mozart-k545.xml` | `Untitled(17).xml` |
| D2 — Mozart low-resolution screenshot | `D2-mozart-k545-screenshot-lowres.xml` | `Untitled(16).xml` |
| E — Chopin scan | `E-chopin-prelude-20.xml` | `Untitled(4).xml` |
| F — complete three-page *Für Elise* PDF | `F-beethoven-fur-elise-full-pdf.xml` | `beethoven-fur-elise-wier-1913.xml` |
| G — hymn scan | `G-hymn-gracious-saviour.xml` | `Untitled(9).xml` |
| G2 — hymn good photo | `G2-hymn-gracious-saviour-photo-good.xml` | `Untitled(8).xml` |
| G3 — hymn bad photo | `G3-hymn-gracious-saviour-photo-bad.xml` | `Untitled(6).xml` |
| H — *Beautiful Dreamer* | `H-foster-beautiful-dreamer.xml` | `Untitled(7).xml` |
| I — *Shenandoah* lead sheet | `I-shenandoah-lead-sheet.xml` | `shenandoah-lead-sheet.xml` |
| J — Beethoven minuet | `J-beethoven-minuet-g.xml` | `Untitled(3).xml` |
| X — unreadable blurred photo | **No export**: app reported `no music found` | — |

Extra app items, excluded from the main 18-upload benchmark:

| Extra item | MusicXML export | Original export name |
|---|---|---|
| Duplicate E import/export | Removed (byte-for-byte duplicate of the E export) | `Untitled(5).xml` |
| F, page 1 imported separately | `F-page1-separate.xml` | `Untitled.xml` |
| F, page 2 imported separately | `F-page2-separate.xml` | `Untitled(2).xml` |
| F, page 3 imported separately | `F-page3-separate.xml` | `Untitled(1).xml` |

The two E exports were byte-for-byte identical. Keep the single-page F files only as diagnostic outputs; the full-PDF export is the benchmark result for F. The X failure is visible in `Screenshot_20261116-112515.png`. The app's item grid is visible in the three screenshots beginning `Screenshot_20261116-112352.png`.

## Run observations

- The operator uploaded each input as supplied, without special cropping or manual processing.
- Recognition felt almost immediate, roughly one second per input. This was a recollection, not a stopwatch measurement, so `seconds` is blank in `../runs.csv`.
- X produced the app status `no music found`. It has no export or valid recognized notes and is recorded as a complete conversion failure. Because X was intentionally unreadable, note-level accuracy on X is not defined; the separate failure-behavior record says it refused rather than invented notes.
- `Screenshot_20261116-111523.png` shows a low-resolution warning, but the saved evidence does not establish which upload triggered it. It has not been assigned to a run.
- The saved XML provides the core transcription evidence. Its normal lyric entries are absent on G, G2, G3, H, and I; its normal chord-symbol entries are absent on I. This establishes what the exported scores retained, without establishing what the app may have displayed internally.
- The benchmark images contain printed fingering on A, B, D, E (in Prelude No. 21), and F. The corresponding exports have 0, 0, 0, 24, and 106 fingering entries respectively; A2 has 0 and A3 has 2. These counts establish export presence, not whether each finger number is correct or aligned to the right note. Alignment and accuracy still need comparison with answer keys.
