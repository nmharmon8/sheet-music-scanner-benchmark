# PlayableNotes benchmark run — 2026-11-16

Run through the web app at dev.playablenotes.com, which serves the same code as production (dev at
`092890bb`). It used a dev account in Chrome, with credits bought by Stripe test card. Each of the 18 uploads was put in once
through **Upload music** as supplied (F as the one three-page PDF), the rights box ticked, **Read** pressed, and the
MusicXML downloaded from **Download** before anything was edited. `seconds` runs from
pressing Read to the score being playable, and is rounded to 5 s. The score links are in the `screenshot` column of `../runs.csv`.

Price: 1 credit per line of music read, $10 for 100 credits (about $0.083 at the 300-credit pack). Lines that fail
are not charged. 125 credits were used in all, which is $12.50 at the $10 price.

What the run showed, before answer keys:

- **E:** only Prelude No. 20 came out (13 bars). The first 8 bars of No. 21 are missing, and no warning was shown.
- **H:** a "1 to check" badge, and only 10 lyric syllables in the export. The voice part is mostly lost.
- **I:** notes, chord symbols and both verses are exact. Segno, To Coda and D.S. al Coda are lost, so playback goes straight through. **J:** repeats and endings are kept, but "Men. da capo" is lost.
- **G:** the previous hymn's last system is left out, and it isn't charged.
- **X:** the upload dialog warned "This photo looks blurry" before reading. The reading then ran for 15 minutes and
  ended with "This music could not be read … (line-timeout)", and the credits were refunded.
- The dialog's "may be cut off at the edge" tip appeared on D (correct, since the scan is cut off) and on C3, A3 and D2.
- **C:** the scan's reading has the intro a step high in places, and the good photo C2 reads it correctly. So a scan
  is not always the easier upload.
