# Same-60 OLiMPiC comparison: PlayableNotes, Sheetly and Audiveris 5.11.0

This folder compares PlayableNotes against Sheetly and Audiveris 5.11.0 on the same 60 OLiMPiC scanned test systems (`samples.txt`), scored with the OLiMPiC authors' TEDn and symbol error rate (SER) code.

## Selection and sources

The 60 systems are the first system (`p1-s1`) of 60 different OLiMPiC test songs — the set Sheetly published raw MusicXML outputs for in [`loveranmar/omr-benchmark`](https://github.com/loveranmar/omr-benchmark/tree/83f007724e16a9fa821f857606156c28a92bc5e9/olimpic60) (folder `olimpic60/`, commit `83f007724e16a9fa821f857606156c28a92bc5e9`). That commit also contains Audiveris 5.11.0 outputs for 50 of the 60 systems; the 10 systems where Audiveris produced no output are scored as empty output, matching the OLiMPiC scorer. Sheetly's and Audiveris's files are not copied into this repository.

PlayableNotes' outputs for the same 60 systems come from the full 1,493-system run in [`../runs/2026-11-19/`](../runs/2026-11-19/).

## Results (lower is better)

| System | TEDn full | TEDn (LMX) | SER | Note error rate | No output |
|---|---:|---:|---:|---:|---:|
| **PlayableNotes** | **12.66%** | **8.45%** | **9.55%** | 3.59% | 0 / 60 |
| Sheetly | 38.78% | 35.92% | 35.68% | 10.24% | 0 / 60 |
| Audiveris 5.11.0 | 45.14% | 42.52% | 47.96% | 53.44% | 10 / 60 |

All three engines' MusicXML exports were canonicalized identically before scoring:

1. `sort_chords.py`: sorts notes within each chord in ascending pitch order.
2. `voice_order.py`: re-serializes each measure voice by voice in time order (MuseScore's canonical order), leaving pitches, durations, chords, beams, ties and notations unchanged.

Without this canonicalization step, Sheetly scores 59.7% TEDn full. Full pooled and per-system scores are in `scores.json`.

## How to reproduce

1. Run `../setup.sh` from the repository root (`olimpic/setup.sh`) to fetch the OLiMPiC scanned dataset and the authors' `olimpic-icdar24` scorer at the pinned commit.
2. Clone `https://github.com/loveranmar/omr-benchmark` and check out commit `83f007724e16a9fa821f857606156c28a92bc5e9` to obtain Sheetly's and Audiveris 5.11.0's MusicXML files under `olimpic60/`. PlayableNotes' predictions for the 60 IDs in `samples.txt` are at `olimpic/runs/2026-11-19/samples/<id>/prediction.musicxml`.
3. Canonicalize every engine's MusicXML file:

```sh
python3 sort_chords.py input.musicxml sorted.musicxml
python3 voice_order.py sorted.musicxml canonical.musicxml
```

4. Linearize each canonical MusicXML file's piano part with the OLiMPiC authors' `Linearizer` and score against the gold `.musicxml` and `.lmx` files using `TEDn_lmx_xml` (`full` and `lmx`) and Levenshtein token distance (SER), pooling edit costs over gold costs across all 60 systems as in `../score.py` (with missing files scored as empty output).
