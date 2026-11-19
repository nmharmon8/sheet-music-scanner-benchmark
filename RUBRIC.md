# Benchmark rubric: what to record

Two kinds of numbers:

- **You record** things only a person at the screen can see: time, cost, warnings, what playback does, effort.
  That's sections 1–4 below, written into `results/runs.csv`.
- **The scorer computes** the accuracy numbers from each tool's exported file and the answer keys (section 5).
  You only have to save the exports.

Each tool gets one run per upload, with no retries. If a run errors out, record the error. Don't try again unless
the site itself was down, and note that if you do.

## 1. Once per tool (`results/tools.csv`)

| field | what to write |
|---|---|
| tool | name |
| date | date of the run |
| plan | free / trial / paid tier name, and what it cost |
| pricing | per page, per upload, subscription (and its limits) |
| inputs | does it take: JPG/PNG photo, PDF, multi-page PDF (yes/no each) |
| exports | MusicXML / MIDI / PDF / none |
| settings | anything you chose before uploading (instrument, "photo mode", etc.); use the defaults where you can |

## 2. Every upload (`results/runs.csv`, one row per tool × upload)

| field | how to record it |
|---|---|
| tool, id | e.g. `playablenotes`, `C3` |
| outcome | `ok` · `partial` (some of the page missing) · `error` · `refused` |
| seconds | from pressing upload to the first moment you can press play (stopwatch; round to 5 s) |
| cost | money or credits this upload used |
| help_needed | anything you had to do besides uploading: crop, rotate, pick staves, split pages (blank if none) |
| warning | exact text of any warning or "low confidence" notice the tool showed (blank if none) |
| systems_missing | how many systems or staves of the page are missing from the result (count by eye against the page) |
| export | file name you saved, e.g. `results/<tool>/C3.musicxml` (also save MIDI if that's all there is) |
| screenshot | `results/<tool>/C3.png`: the tool's view of the result, every page |

Save the export **before** touching anything in the tool's editor.

## 3. Checks by eye or ear (same row, only for the uploads listed)

Some exports drop fingering, lyrics or chord symbols even when the tool shows them, so check these on screen.
Score each one **2** (all right), **1** (some there or some wrong), **0** (missing or mostly wrong), or **n/a**.

| check | uploads | what counts as 2 |
|---|---|---|
| fingering_shown | A, A2, A3, B, D, F | fingers shown on the right notes; the tuplet 3 in A isn't a finger |
| lyrics_shown | G, G2, G3, H, I | every verse present, under the right notes, verses not mixed |
| chords_shown | I | every chord symbol present, on the right beat (incl. G/B, and Em→A7 mid-measure) |
| play_order | A, B, C, F, I, J | playback follows the page's repeats and jumps (expected order is in `index.json`, `playOrder`) |
| decoys_ignored | C3, G3, A3, D, G, H | no notes from the other page in the frame, from D's ossia staff, or from G's previous hymn mixed into the piece |
| x_result | X | not scored since 2026-11-17 (a reader should always do its best; scoring refusals rewarded giving up) |

For play_order you don't need to listen to the whole piece. Play from just before each repeat or jump and check
where it goes: A's repeat, F's two first/second endings, I's To Coda and D.S. al Coda, and J's endings and da capo.

## 4. Effort to correct (A, C, G, H, I only)

In the tool's own editor, fix the result until it matches the page, with a **15-minute cap** per upload.

| field | how to record it |
|---|---|
| fix_minutes | minutes until it's all right, or 15 if capped |
| fix_edits | rough count of edits (each note, chord, mark or verse changed) |
| fix_done | `yes` if fully fixed, otherwise a rough % fixed |
| fix_blockers | anything the editor couldn't do at all (e.g. no way to add lyrics or fingering) |

## 5. Computed later by the scorer (nothing to record)

From the exported file against the answer key, for every upload:

| score | what it measures |
|---|---|
| measures_clean | share of measures that are entirely right: **the headline** |
| note_f1 | note accuracy, and separately pitch, rhythm, staff/voice, measure |
| notation | key/time signatures and changes, clefs, accidentals, ties, tuplets, grace notes, ornaments, fermatas |
| expression | dynamics, articulations, tempo, pedal (weighted lower) |
| lyrics / fingering / chords | alignment to the right note, when the export carries them |
| structure | repeats, endings, jumps as written in the file |
| robustness | the same scores on C/C2/C3, G/G2/G3, A/A2/A3, D/D2: how far each falls from scan to bad photo |

## 6. The scorecard

Per tool, reported side by side, with no single blended number unless we want one for marketing:

1. Measures clean (all uploads; also split by scan / good photo / bad photo)
2. Note accuracy
3. Structure: play_order passes out of 6
4. Lyrics, fingering, chords (from the export where possible, otherwise from the by-eye checks)
5. Robustness: accuracy drop from scan to bad photo
6. Failure: systems missing, warnings shown
7. Effort: total fix minutes on the five pages
8. Speed (median seconds) and cost per page

If a blended score is wanted: measures clean 35%, structure 15%, lyrics 10%, fingering 10%, robustness 10%,
effort 10%, chords 5%, failure 5%.
