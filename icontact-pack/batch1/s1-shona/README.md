# S1 Shona version: ready for your recording

The pack keeps the same edit as S1 with a Shona voiceover and Shona captions that Kevin supplies and approves.
(This is an approved exception to the English-only rule in CLAUDE.md, per the production pack.)

To make it:
1. Record the four S1 lines in Shona, one file per line: `1.mp3` … `4.mp3` (same order as S1).
2. Send the approved Shona caption text for each line.
3. I copy `../s1-10-second-test` here, put the Shona captions in `ad.json` → `shots[].line`, and run
   `python3 icontact-pack/tools/build.py icontact-pack/batch1/s1-shona --vo <folder with 1.mp3…4.mp3> --alt icontact-pack/batch1/4x5/s1-shona`.
   The cut re-times itself to your recording; the on-screen text stays as approved (send Shona on-screen text too if wanted).
