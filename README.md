# Chess PGN to Docx

## What this site provides 
- a script that generates DOCX file from one chess PGN match, with a chessboard for each half-move, using True Type Font Chess Merida. 

## My intention
... was to support myself learning chess by studying chess games offline form selected PGN printouts.

For online studies a good starting point learning chess is [lichess.org](https://lichess.org/) or others.

This approach provides a printout in B/W with more contrast as the colored PDFs at [lichess_puzzles_to_pdf](https://github.com/hlotze/lichess_puzzles_to_pdf).

## Steps
- install the True Type Font Chess Merida ono your system.
- check the PGN[^1] example
- check the DOCX example
- run the Python script(s)

## Open item
- [ ] finitalize the project with
  - [x] `chess.Board` to chessboard array - done; see `chessboard.board2arr(board)`
  - [ ] a complete docx paragraph with the chessboard in TTF, the PGN of the move and the marked check, from/to-move
  - [ ] a transfer of one complete PGN match to one document
- [ ] add some manual comments or automatically generated comments to each puzzle's move; e.g. by means of [`python-chess`](https://python-chess.readthedocs.io/en/latest/) accessing the [Stockfish](https://stockfishchess.org/) engine
- [ ] refactor coding to get aligned to [`python-chess`](https://python-chess.readthedocs.io/en/latest/) naming conventions and structures
- [ ] add unit tests

## Contact
[@hlotze](https://github.com/hlotze)

[^1]: PGN - see [Wikipedia Portable Game Notation](https://en.wikipedia.org/wiki/Portable_Game_Notation)


