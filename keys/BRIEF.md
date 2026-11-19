# How the answer keys were made

One Claude Opus 5.5 agent per piece wrote the key for its page:

- It read the page at high resolution (`src/`), not the 200 dpi benchmark upload in `../pages/`.
- It never saw any tool's output, PlayableNotes' included, while writing the key.
- A public reference edition could be used as a cross-check; the printed page wins wherever they differ.
- It wrote down exactly what the page prints: every note's pitch, start and length, ties, voices, clefs, key and time
  signatures, repeats and endings, fingering, lyrics and chord symbols. Anything printed that a key can't hold is
  listed in the piece's `.notes.md`.
- The key was then rendered and compared with the page measure by measure, in several verification rounds by fresh
  agents, until a round found nothing to fix.

The keys are in `musicxml/`; `AUDIT.md` checks the bars most likely to be wrong in PlayableNotes' favour.
