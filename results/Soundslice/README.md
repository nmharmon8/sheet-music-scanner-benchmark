# Soundslice image-import benchmark — 2026-11-16

The user's paid Soundslice account was used in Chrome. All 18 benchmark uploads in
`../../index.json` were submitted as supplied, and the exported MusicXML files are
in this directory. The three-page *Für Elise* PDF was uploaded once with all three
pages selected. No source image was cropped, rotated or repaired before upload.

Soundslice processed the images through a review flow before creating each playable
slice. Preselected answers were accepted throughout, except where the flow required
an explicit answer (listed below). The initial C upload was interrupted by the
operator navigating away while the upload was still in progress; there was no saved
result from that attempt, so it was submitted again and exported. All other inputs
had one submitted run. No imported score was edited before MusicXML export.

The import page showed **20 of 100 available pages used this month** after the
benchmark: 17 single-page uploads plus the three-page PDF. The plan's exact tier,
subscription price and billing period were not verified. The editor offered
MusicXML, PDF, GPX, MIDI and MP3 export; MusicXML is the saved benchmark output.

## Exports

The counts below are XML elements, not accuracy scores. `Notes` counts pitched
`<note>` elements, excluding rests. The scorer still needs answer keys to determine
whether notes, fingering, lyrics or chords match the printed page.

| Input | Slice | Pitched notes | Fingerings | Lyrics | Chords | Review observations |
|---|---|---:|---:|---:|---:|---|
| A | [Kuhlau](https://www.soundslice.com/slices/kwBBc/) | 545 | 134 | 0 | 0 | Defaults; many fingering/articulation questions |
| B | [Schumann](https://www.soundslice.com/slices/qwBBc/) | 354 | 116 | 0 | 0 | Defaults |
| C | [Joplin](https://www.soundslice.com/slices/PwBBc/) | 290 | 0 | 0 | 0 | Defaults; interrupted first attempt noted above |
| D | [Mozart](https://www.soundslice.com/slices/FwBBc/) | 332 | 94 | 0 | 0 | Explicit treble-clef choice for the small ossia staff |
| E | [Chopin](https://www.soundslice.com/slices/NYBBc/) | 392 | 42 | 0 | 0 | Defaults |
| F | [Für Elise](https://www.soundslice.com/slices/TYBBc/) | 907 | 164 | 0 | 0 | Complete three-page PDF; defaults |
| G | [Hymn](https://www.soundslice.com/slices/1YBBc/) | 255 | 0 | 211 | 0 | Defaults; export includes words from preceding hymn |
| H | [Beautiful Dreamer](https://www.soundslice.com/slices/7YBBc/) | 187 | 0 | 38 | 0 | Defaults, including added-staff questions |
| I | [Shenandoah](https://www.soundslice.com/slices/9YBBc/) | 40 | 0 | 78 | 16 | Defaults; no segno/coda or D.S. events in export |
| J | [Beethoven minuet](https://www.soundslice.com/slices/nYBBc/) | 332 | 0 | 0 | 0 | Defaults |
| C2 | [Joplin good photo](https://www.soundslice.com/slices/5YBBc/) | 290 | 0 | 0 | 0 | Defaults |
| C3 | [Joplin bad photo](https://www.soundslice.com/slices/GYBBc/) | 290 | 0 | 0 | 0 | Defaults; inclusion questions |
| G2 | [Hymn good photo](https://www.soundslice.com/slices/hYBBc/) | 255 | 0 | 196 | 0 | Defaults |
| G3 | [Hymn bad photo](https://www.soundslice.com/slices/DlBBc/) | 254 | 0 | 196 | 0 | Explicit note-position choice on another page in the frame |
| A2 | [Kuhlau good photo](https://www.soundslice.com/slices/YlBBc/) | 545 | 134 | 0 | 0 | Defaults; many review questions |
| A3 | [Kuhlau bad photo](https://www.soundslice.com/slices/TlBBc/) | 545 | 132 | 0 | 0 | Defaults; 11 review screens and many questions |
| D2 | [Mozart low-resolution screenshot](https://www.soundslice.com/slices/8lBBc/) | 332 | 91 | 0 | 0 | Explicit treble-clef choice for the small ossia staff |
| X | [Unreadable control](https://www.soundslice.com/slices/BlBBc/) | 10 | 0 | 0 | 0 | Explicit bass-clef choice; then playable music without a visible low-confidence warning |

All 18 MusicXML files parse as `score-partwise`. The values above come from the
saved exports. They establish that the format preserves *some* printed fingering,
lyrics and chord symbols. They do not establish that these are complete or aligned
correctly. For example, the G scan's 211 lyric elements include a fifth verse
number from the preceding hymn; the G photo exports have four verse numbers.
The H export has one verse number. These are concrete points for later scoring.

The I export has 15 measures and chord/lyric elements, but no MusicXML segno, coda,
`D.S.`, or `To Coda` directions. Its answer key contains those jump directions.
The F export has three repeat elements and eight ending elements; J has six repeats
and eight endings. These element counts alone do not establish correct play order.

## Unreadable control

X was deliberately blurred so that it has no readable note-level ground truth.
Soundslice did not refuse it: the review flow asked for a lower-staff clef, and the
operator selected bass clef based on the known underlying source. It then created a
playable slice and exported 10 pitched notes across four measures, without a visible
low-confidence warning. Record this as `music without warning` with **manual clef
assistance**, not as an unassisted recognition result. X is excluded from note
accuracy denominators under the rubric.

## Timing and remaining work

The `seconds` entries in `../runs.csv` are approximate upload-to-playable times,
rounded to five seconds, for the five variants where that interval was captured
end-to-end: C2 20 s, C3 25 s, G2 25 s, A2 85 s, A3 65 s. They include the time spent
accepting review questions. Other timings were not measured consistently, so their
cells are blank. The PDF imports F and I each took roughly two minutes to reach
review-ready; these are observations, not stopwatch-comparable upload-to-playable
measurements.

The source score keys for A–H and J still need to be made before objective note and
measure accuracy can be calculated. `../../keys/shenandoah-lead-sheet.musicxml` is
the existing key for I. Optional playback checks and timed manual correction tasks
from the rubric were not performed. Blank cells in `../runs.csv` mean unmeasured,
not a zero score or a failed feature.
