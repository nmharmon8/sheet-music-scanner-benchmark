# Sheet music scanner benchmark: piano OMR accuracy, 7 apps, 17 uploads

How accurately do sheet music scanner apps (optical music recognition, OMR) read printed piano music? We ran the same
17 uploads (made from 10 piano pieces) through seven readers, one scored export per tool per upload: **PlayableNotes, Soundslice, Songscription,
Halbestunde, Scan2Notes, PlayScore 2 and Sheet Music Scanner**. Then we scored every exported MusicXML file bar by
bar against checked answer keys with one scorer. Everything needed to check the numbers is in this repository:
the uploads, the answer keys, every tool's raw export, the scorer, and the per-upload scores. We also ran PlayableNotes
on [OLiMPiC](https://github.com/ufal/olimpic-icdar24), a public piano OMR test set from Charles University, and
scored it with that dataset's own TEDn scorer; those 300 predictions are here too.

**Conflict of interest:** PlayableNotes is our product (Ozni Apps LLC). Read this as a vendor's benchmark, and check
it: the scorer runs in seconds on the files here (`python3 score.py`), and any upload can be re-run through any app.

Run dates: competitors 16 November 2026 (each in its own app), PlayableNotes 18 November 2026. Summary page:
[playablenotes.com/sheet-music-scanner-benchmark](https://playablenotes.com/sheet-music-scanner-benchmark).

## Results: bars read exactly right

A bar counts only if every pitch, onset and length in it matches the answer key. Figures are the mean over the 17
uploads of each upload's share of bars read exactly right (higher is better). "Bars exact (pooled)" counts all bars
together.

| Reader | All 17 uploads | Scans and the lead sheet (10) | Good phone photos (3) | Bad phone photos (3) | Low-res screenshot (1) | Bars exact (pooled) | Note F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **PlayableNotes** (18 Nov 2026) | **97.7%** | **98.5%** | **98.4%** | **93.8%** | **100%** | 458 of 469 | 0.997 |
| Soundslice | 89.4% | 89.1% | 92.8% | 87.1% | 89.5% | 419 of 457 | 0.950 |
| Songscription | 78.7% | 82.3% | 96.7% | 59.0% | 47.4% | 366 of 469 | 0.895 |
| Halbestunde | 73.0% | 72.8% | 73.4% | 74.8% | 68.4% | 332 of 461 | 0.893 |
| Scan2Notes | 71.7% | 70.2% | 73.4% | 76.2% | 68.4% | 324 of 457 | 0.886 |
| PlayScore 2 | 37.5% | 53.5% | 31.6% | 2.4% | 0.0% | 237 of 469 | 0.777 |
| Sheet Music Scanner | 17.7% | 29.4% | 2.4% | 0.0% | 0.0% | 110 of 461 | 0.629 |

PlayableNotes has the highest average on these uploads. Its lead over Soundslice is 8.3 points: 95% interval 2.0 to
16.3 points resampling the 17 uploads, 1.5 to 17.4 resampling the 10 pieces (`python3 ci.py`); better on 10 uploads,
tied on 5, worse on 2; 5.1 points with the voice-and-piano upload H left out. PlayableNotes' first, blind reading of
the set scored 82.3%, 7.1 points behind Soundslice (95% interval -19.4 to +3.0): see the runs below.

The pooled bar totals differ between tools because the hymn page (G) prints the end of the previous hymn above it, and
each tool is scored on the 12-bar key (the hymn alone) or the 16-bar key (with the previous hymn's end), whichever
gives it the higher bars-exact plus note F1 (`score.py`; `diffbars.py` chooses the same way). On the 16-bar key for
everyone Soundslice would score 85.5%; on the 12-bar key, PlayableNotes 97.6% and Soundslice 89.4%. The order is the
same either way. 469 bars are scored in all, 304 distinct bars from the 10 pieces.

### Four full-set PlayableNotes runs

The other six tools were each run once. PlayableNotes was run four times as it was developed; all four are here. The
first, through the website, was the first look at these uploads. What it got wrong guided later changes, which were
tested on other pages before this set was read again, so the later readings are less blind than the competitors'
single runs. Partial reruns of a few uploads, made while diagnosing errors, aren't included.

| Date | Reading | Folder | Bars exact |
|---|---|---|---:|
| 16 Nov 2026 | Through the website | `results/PlayableNotes-before-20261116/` | 82.3% |
| 17 Nov 2026 | Production release of that day, run locally | `results/PlayableNotes-release-20261117/` | 94.4% |
| 17 Nov 2026 | Development pipeline of that day, run locally | `results/PlayableNotes-20261117/` | 95.7% |
| 18 Nov 2026 | Production release of that day, run locally (the scored entry) | `results/PlayableNotes/` | 97.7% |

Other measures (F1 from 0 to 1, or share kept). Navigation marks are the segno, To Coda, coda and D.S. al Coda on
the lead sheet (I), the only upload with them, checked in each export, not in each tool's playback:

| Reader | Fingering F1 | Lyrics F1 | Chord symbols F1 | Repeats and endings kept | Navigation marks kept (lead sheet I) |
|---|---:|---:|---:|---:|---:|
| PlayableNotes | 0.98 | 0.99 | 1.00 | 1.00 | 1.00 |
| Soundslice | 0.95 | 0.91 | 0.94 | 1.00 | 0.00 |
| Songscription | 0.59 | 0.98 | 1.00 | 0.88 | 0.50 |
| Halbestunde | 0.00 | 0.90 | 0.94 | 0.55 | 0.50 |
| Scan2Notes | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| PlayScore 2 | 0.14 | 0.00 | 0.00 | 0.47 | 0.25 |
| Sheet Music Scanner | 0.00 | 0.00 | 0.00 | 0.56 | 0.00 |

Per upload (bars exact, %):

| Upload | Bars | PlayableNotes | Soundslice | Songscription | Halbestunde | Scan2Notes | PlayScore 2 | Sheet Music Scanner |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A Kuhlau, Sonatina Op. 20 No. 1 (scan) | 41 | 100 | 98 | 54 | 66 | 66 | 88 | 22 |
| B Schumann, The Merry Peasant (scan) | 21 | 95 | 95 | 100 | 100 | 95 | 43 | 43 |
| C Joplin, The Entertainer (scan) | 16 | 100 | 100 | 100 | 100 | 94 | 25 | 0 |
| D Mozart, K. 545 (scan) | 19 | 100 | 89 | 47 | 53 | 53 | 47 | 5 |
| E Chopin, Preludes 20 and 21 (scan) | 21 | 100 | 86 | 43 | 43 | 38 | 86 | 33 |
| F Beethoven, Für Elise, 3-page PDF | 106 | 98 | 96 | 97 | 70 | 71 | 81 | 45 |
| G Hymn, Gracious Saviour (scan) | 16 | 100 | 100 | 94 | 67 | 67 | 0 | 0 |
| H Foster, Beautiful Dreamer, voice and piano (scan) | 12 | 100 | 42 | 100 | 33 | 33 | 0 | 0 |
| I Shenandoah lead sheet (vector PDF) | 17 | 100 | 88 | 94 | 100 | 100 | 94 | 100 |
| J Beethoven, Minuet in G (scan) | 35 | 91 | 97 | 94 | 97 | 86 | 71 | 46 |
| C2 The Entertainer, good photo | 16 | 100 | 100 | 100 | 100 | 100 | 31 | 0 |
| C3 The Entertainer, bad photo | 16 | 88 | 100 | 94 | 94 | 94 | 0 | 0 |
| G2 Hymn, good photo | 16 | 100 | 83 | 100 | 67 | 67 | 0 | 0 |
| G3 Hymn, bad photo | 16 | 94 | 83 | 69 | 62 | 67 | 0 | 0 |
| A2 Kuhlau, good photo | 41 | 95 | 95 | 90 | 54 | 54 | 63 | 7 |
| A3 Kuhlau, bad photo | 41 | 100 | 78 | 15 | 68 | 68 | 7 | 0 |
| D2 Mozart, 800 px screenshot | 19 | 100 | 89 | 47 | 68 | 68 | 0 | 0 |

PlayableNotes is not best on every upload: Soundslice did better on J and C3, and Songscription and Halbestunde on B.
On C3, for example, Soundslice got all 16 bars and PlayableNotes 14: `python3 diffbars.py PlayableNotes C3`.

## OLiMPiC (a public test set by other researchers)

[OLiMPiC](https://github.com/ufal/olimpic-icdar24) (Mayer, Straka, Hajič jr., Pecina, *Practical End-to-End Optical
Music Recognition for Pianoform Music*, ICDAR 2024) has 1,493 piano systems cut from real IMSLP scans of
19th-century songs, each with a hand-made MusicXML answer. Scoring is the authors' own code: TEDn, a normalized tree
edit distance between the predicted and the true MusicXML (roughly, the share of the score that needs editing).
Lower is better.

| System | Test systems | TEDn full | TEDn (LMX) | Symbol error rate |
|---|---|---:|---:|---:|
| PlayableNotes (18 Nov 2026) | fixed sample of 300 | 14.05% | 9.87% | 11.82% |
| Zeus, the dataset authors' model (paper, Table 3) | all 1,493 | 18.40% | 14.85% | 17.72% |

- The sample (`olimpic/sample.txt`) is 3 systems from each of the 100 test songs: those with the lowest SHA-256 of
  their id, fixed before any run.
- Every prediction is in `olimpic/runs/2026-11-18/samples/<song>/<system>/`: `prediction.musicxml` (what was
  scored), `tedn.json` (the scores) and `result.json` (whether it produced output, measures and seconds).
  To score them yourself: `olimpic/setup.sh` (fetches the dataset and the authors' scorer at a pinned commit), then
  `olimpic/.venv/bin/python olimpic/score.py 2026-11-18`, which scores every prediction again
  with the authors' TEDn (slow; `--cached` reuses the committed `tedn.json` files). Exact figures: TEDn full 14.05%,
  TEDn (LMX) 9.87%, SER 11.82%.

## Method

1. **The uploads** (`pages/`, described in `index.json`): nine US public-domain scans published 1864 to 1919, from IMSLP
   and the Internet Archive, and a *Shenandoah* lead sheet engraved for the test (a vector PDF; counted with the scans) (edition, plate number and source link for each in `index.json`), chosen to test several
   things at once: fingering, lyrics in several verses, chord symbols, repeats with first and second endings, D.S. al
   Coda and da capo, ornaments, clef changes, a second piece starting mid-page, a three-page PDF, voice and piano on
   three staves, and an older page with show-through. Three of them (C, G, A) were also made into a good phone photo
   and a bad phone photo with another page in the frame, and one (D) into an 800-pixel screenshot. The photos are
   synthetic, made from the scans with perspective, page curl, a shadow, warm uneven light, a table around the page, blur, noise and JPEG compression (the files in `pages/` are exactly what each tool got). A blurred photo that can't be read (X)
   was run but is not scored.
2. **The answer keys** (`keys/`): one per piece, drafted by an AI agent from the high-resolution sources in `keys/src/`
   (a public reference edition was allowed as a starting point; the printed page wins wherever they differ), never
   seeing any tool's output (`keys/BRIEF.md`), then rendered and checked measure by measure in several verification
   rounds. The agents were Claude Opus 5.5.
   `python3 audit.py` lists the key bars most likely to be wrong in PlayableNotes' favour; `keys/AUDIT.md` checks them
   (none on the scans; 7 on two photos and the screenshot, where Halbestunde, Scan2Notes (one engine) and Sheet Music
   Scanner read a treble-clef staff as bass clef). The keys are MusicXML (`keys/musicxml/`).
3. **Running the tools** (`RUBRIC.md`, `results/runs.csv`, `results/tools.csv`): each competitor read each upload once,
   as supplied, and its MusicXML export was saved before any editing. Soundslice's first upload of C was interrupted
   before it finished and was run again; Sheet Music Scanner's settings weren't recorded.
   Competitors ran in their own apps on 16 November 2026, on paid plans where the free tier didn't allow the test.
   Soundslice asked questions on D, D2 and G3 that had to be answered by hand; its other offered options were left at
   their defaults (`results/tools.csv`).
   PlayableNotes read each upload once with its production release of 18 November 2026, exported with the same
   converter as the website's MusicXML download.
4. **Scoring** (`score.py`, Python standard library only): every export, ours included, is converted to one neutral
   list of notes and scored against the key the same way. Measures are aligned in order first; a key bar counts when a
   bar of the export matches it exactly (every note's pitch, onset and length). Extra bars in an export are not counted
   against it. Note F1 matches notes in order on pitch and length. Fingering is F1 over (note, finger)
   pairs in order; lyrics over syllables in order, verse by verse; chord symbols over the symbols in order; repeats are the count of repeat signs and endings in the export against the key's, capped at 1 (counted, not matched in place); jumps are the share of the lead sheet's four navigation marks kept. The header of
   `score.py` lists every normalization (pickup bars, bars split at a repeat, a note shared by two voices). Run
   `python3 diffbars.py <Tool> <id>` to see exactly which bars a tool got wrong.

## Limits

- 17 uploads is a small set, chosen to test many things at once, not a random sample of printed music. It is piano
  (and voice-and-piano) music only: no orchestral scores, guitar tab or handwriting.
- PlayableNotes made the answer keys (with an AI agent, checked in verification rounds).

## Files

```
pages/             the uploads, exactly as given to every tool
index.json         each upload: source, edition, licence, what is on the page, which measures it feeds
keys/              answer keys (keys/musicxml/), high-resolution sources (keys/src/), brief
results/<Tool>/    each tool's raw MusicXML export, unedited
results/scores.csv every score per tool and upload; scores.json the same with the summary
results/runs.csv   per run: seconds, warnings, what the tool showed; tools.csv: plan, inputs, settings
score.py           the scorer (with analyze.py); diffbars.py shows the bars a tool got wrong; ci.py the intervals;
                   audit.py the key bars to check (keys/AUDIT.md)
make_plots.py      writes results/plots.html
olimpic/           the OLiMPiC sample, PlayableNotes' 300 predictions, and the authors' scorer setup
```

## Reproduce

```sh
python3 score.py                          # results/scores.json and scores.csv from results/ and keys/ (seconds)
python3 ci.py                             # 95% intervals for the differences between tools
python3 diffbars.py Soundslice H          # which key bars a tool got wrong on one upload
python3 make_plots.py                     # results/plots.html
```

To test another reader: run each file in `pages/` through it once, export MusicXML into `results/<YourTool>/` with the
same file names, and run `score.py`. Corrections and new results are welcome as issues or pull requests, or by email
to support@playablenotes.com.

## Tools not tested

ScanScore, SmartScore, PhotoScore, Audiveris (and MuseScore's import, which uses it) and ScoreLens were not run in
this round. The uploads, keys and scorer are here so that anyone can add them: export MusicXML into
`results/<Tool>/` and run `score.py`.

## Licence

The scans are US public domain. The answer keys, scores, documentation and PlayableNotes' outputs are CC BY 4.0;
the scripts are MIT (`LICENSE`). The other tools' exports are their output for these public-domain pages, included
unedited so the scores can be checked. OLiMPiC's data is not included; `olimpic/setup.sh` fetches it from its
authors (CC BY-SA 4.0).
