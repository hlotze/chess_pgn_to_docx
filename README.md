# Chess PGN to Docx

## What this site provides 
- a script `chess_pgn_to_docx.py`  that generates one DOCX file from one chess PGN[^1] match, with a chessboard for each half move, using True Type Font Chess Merida. 
  - ensure that you installed the TTF[^5] Chess Merida, which is given e.g. at `TTF/` directory.
  - the script processes all `*.pgn` files that it find at `PGN/` directory.
  - be aware, a PGN file can have thousends of games inside, and with this script each of its games will get a DOCX file in `DOCX/` directory
  - each game's DOCX generation take about 1 second (on my old machine.)
  - the script was not possible without [`python chess`](https://github.com/niklasf/python-chess) and [`python docx`](https://github.com/python-openxml/python-docx)

## My intention
... was to support myself learning chess by studying chess games offline form selected PGN printouts.

For online studies a good starting point learning chess is [lichess.org](https://lichess.org/) or others.

This approach provides a printout in B/W with more contrast as the colored PDFs at [lichess_puzzles_to_pdf](https://github.com/hlotze/lichess_puzzles_to_pdf).

## Steps
- install the True Type Font (TTF) Chess Merida onto your system; see `TTF/`
- check 
  - the PGN[^1] examples; see `PGN/`
  - the DOCX examples; see `DOCX/`
  - your env: needed imports are listed within the script, env. req. will be provided soon
- run the Python script `chess_pgn_to_docx.py`

## Open item
- [x] finitalize the project - initially done
- [x] add unit tests - initially done, to be completed
- [x] fix problems with file names if *Seven Tag Roster* (details at [^1]) is incomplete, e.g. with older games
- [ ] add some word's about the game's ECO[^2]
- [ ] mark a checked king at the diagrams
- [ ] mark the from- and to-squares of a half move
- [ ] add [%eval ...] comments [^3] to the SAN[^4] at bottom of a board
- [ ] add 
  - [ ] env requirements
  - [ ] tests
  - [ ] packageing
  - [ ] documentation
- [ ] evtl. refactor coding to get aligned to [`python-chess`](https://python-chess.readthedocs.io/en/latest/) naming conventions and structures

## Contact
[@hlotze](https://github.com/hlotze)

## Footnotes
[^1]: PGN - see [Wikipedia Portable Game Notation](https://en.wikipedia.org/wiki/Portable_Game_Notation)

[^2]: ECO - see [Wikipedia: Encyclopaedia of Chess Openings](https://en.wikipedia.org/wiki/List_of_chess_openings) or a [Detailed opening library](https://www3.diism.unisi.it/~addabbo/ECO_aperture_scacchi.html)

[^3]: chess evaluation - see [chessprogramming.org/Evaluation](https://www.chessprogramming.org/Evaluation)

[^4]: SAN - see [Wikipedia: Algebraic_notation_(chess)](https://en.wikipedia.org/wiki/Algebraic_notation_(chess))

[^5]: TTF - see [Wikipedia: TrueType](https://en.wikipedia.org/wiki/TrueType)


