"""functions for chessboard mgmt, and TTF mapping"""
from __future__ import print_function

import chess
import numpy as np


# chessboard:  white view
#    top    files black pieces - lowercase chars,
#    bottom files white pieces - uppercase chars
#
# tl -- -- -- -- -- -- -- -- tr
# 8| rw nb bw qw kw bb nw rb ||  # |x that marks the site to move, at file 8 --> black
# 7| pb pw pb pw pb pw pb pw ||
# 6| -w -b -w -b -w -b -w -b ||
# 5| -b -w -b -w -b -w -b -w ||
# 4| -w -b -w -b -w -b -w -b ||
# 3| -b -w -b -w -b -w -b -w ||
# 2| Pw Pb Pw Pb Pw Pb Pw Pb ||
# 1| Rb Nw Bb Qw Kb Bw Nb Rw ||  # |x that marks the site to move, at file 1 --> white
# bl a- b- c- d- e- f- g- h- br


# These TTF works with the mapping at 'font_dict',
# I prefer 'Chess Merida'
TTF_dict = {
    'Chess Condal': 'CONDFONT.TTF',
    'Chess Kingdom': 'KINGFONT.TTF',
    'Chess Leipzig': 'LEIPFONT.TTF',
    'Chess Merida': 'MERIFONT.TTF'
}
# docu and mapping see: https://candyfonts.com/font/chess-leipzig.htm
# codes are for usage in
#   MS Word or
#   LibreOffice Writer
#
# if using for HTML generation
# you may add to your HTML page
#
#   <style type="text/css">
#     @font-face {
#       font-family:"chess-leipzig";
#       src:url("https://candyfonts.com/wp-data/2019/03/03/22938/LEIPFONT.TTF") format("woff"),
#       url("https://candyfonts.com/wp-data/2019/03/03/22938/LEIPFONT.TTF") format("opentype"),
#       url("https://candyfonts.com/wp-data/2019/03/03/22938/LEIPFONT.TTF") format("truetype");
#     }
#     htm_tag{font-family:"chess-leipzig";font-size:40px;text-transform:none;color:#F32951}
#   </style>
#
# and translate e.g. the given '\x20' to HTML '&#x20;'

# these maping to use e.g.
#
#   import codecs
#   print(codecs.decode(b'\xf1\xf2\xf3\xf4', 'iso-8859-9') )

font_dict = {
    # squares
    #   1st char --> piece
    #   2nd char --> square color b_lack or w_hite
    #
    # empty white square - no piece, white square
    '-w': '\x2a',
    # dot marked white square
    'ow': '\x2e',
    # x marked white square
    'xw': '\x78',
    # white pieces, white square
    'Kw': '\x6b',  # K_ing
    'Qw': '\x71',  # Q_ueen
    'Rw': '\x72',  # R_ook
    'Bw': '\x62',  # B_ishop
    'Nw': '\x6e',  # k_N_ight
    'Pw': '\x70',  # P_awn
    # black pieces, white square
    'kw': '\x6c',  # k_ing
    'qw': '\x77',  # q_ueen
    'rw': '\x74',  # r_ook
    'bw': '\x76',  # b_ishop
    'nw': '\x6d',  # k_n_ight
    'pw': '\x6f',  # p_awn

    # empty black square - no piece, black square
    '-b': '\x2b',
    # dot marked black square
    'ob': '\x3a',
    # x marked black square
    'xb': '\x58',
    # white pieces, black sqare
    'Kb': '\x4b',  # K_ing
    'Qb': '\x51',  # Q_ueen
    'Rb': '\x52',  # R_ook
    'Bb': '\x42',  # B_ishop
    'Nb': '\x4e',  # k_N_ight
    'Pb': '\x50',  # P_awn
    # black pieces. black square
    'kb': '\x4c',  # k_ing
    'qb': '\x57',  # q_ueen
    'rb': '\x54',  # r_ook
    'bb': '\x56',  # b_ishop
    'nb': '\x4d',  # k_n_ight
    'pb': '\x4f',  # p_awn
    # figurine pieces - with piece independed of color
    'fk': '\xa2',  # king
    'fq': '\xa3',  # queen
    'fr': '\xa6',  # rook
    'fb': '\xa5',  # bishop
    'fn': '\xa4',  # knight
    'fp': '\xa7',  # pawn

    # Borders
    'tl':  '\x31',   # corner at top left
    'tr':  '\x33',   # corner at top right
    'bl':  '\x37',   # corner at bottom left
    'br':  '\x39',   # corner at bottom right
    '--':  '\x32',   # top border
    '||':  '\x35',   # standard border right

    # not available with chess leipzig
    # just a best match - do not use!
    '|x':  '\x25',   # standard border right marks the site to move
    #   at file 8 --> black
    #   at file 1 --> white

    'a-':  '\xc8',   # bottom border for rank a
    'b-':  '\xc9',   # bottom border for rank b
    'c-':  '\xca',   # bottom border for rank c
    'd-':  '\xcb',   # bottom border for rank d
    'e-':  '\xcc',   # bottom border for rank e
    'f-':  '\xcd',   # bottom border for rank f
    'g-':  '\xce',   # bottom border for rank g
    'h-':  '\xcf',   # bottom border for rank h
    '1|':  '\xc0',   # left border for file 1
    '2|':  '\xc1',   # left border for file 2
    '3|':  '\xc2',   # left border for file 3
    '4|':  '\xc3',   # left border for file 4
    '5|':  '\xc4',   # left border for file 5
    '6|':  '\xc5',   # left border for file 6
    '7|':  '\xc6',   # left border for file 7
    '8|':  '\xc7'    # left border for file 8
}


# the chessboard from White view; as str
# ranks: 8 ... 1
# files: a ... h
START_WHITE_STR = \
    'tl -- -- -- -- -- -- -- -- tr \n' + \
    '8| rw nb bw qb kw bb nw rb || \n' + \
    '7| pb pw pb pw pb pw pb pw || \n' + \
    '6| -w -b -w -b -w -b -w -b || \n' + \
    '5| -b -w -b -w -b -w -b -w || \n' + \
    '4| -w -b -w -b -w -b -w -b || \n' + \
    '3| -b -w -b -w -b -w -b -w || \n' + \
    '2| Pw Pb Pw Pb Pw Pb Pw Pb || \n' + \
    '1| Rb Nw Bb Qw Kb Bw Nb Rw || \n' + \
    'bl a- b- c- d- e- f- g- h- br \n'


def str2arr(cb_str: str) -> np.ndarray:
    """Return the chessboard string as ndarray (10,10)"""
    cb_tmp = str(cb_str).replace('\n', '', -1).replace(' ', '', -1)
    cb_arr = np.array(
        [cb_tmp[i:i+2] for i in range(0, len(cb_tmp), 2)]
    ).reshape((10, 10))
    return cb_arr


def arr2str(cb_arr: np.ndarray, sep=' ') -> str:
    """Return the chessboard ndarray as string"""
    cb_str = ''
    for file in range(10):
        line = ''
        for rank in range(10):
            line += cb_arr[file, rank] + sep
        cb_str += line + '\n'
    return cb_str


def arr_flip(cb_arr: np.ndarray) -> np.ndarray:
    """Return the chessboard ndarray
       as flipped ndarray (10,10)"""
    cb_arr_flipped = np.full((10, 10), '__').reshape(10, 10)
    # flip the squares
    cb_arr_flipped[1:9, 1:9] = np.flip(cb_arr[1:9, 1:9])
    # take the top border - unchanged
    cb_arr_flipped[0, 0:10] = cb_arr[0, 0:10]
    # take the right border unchanged
    cb_arr_flipped[1:10, 9] = cb_arr[1:10, 9]
    # flip left border's file names
    cb_arr_flipped[1:9, 0] = np.flip(cb_arr[1:9, 0])
    # take lower left border - unchanged
    cb_arr_flipped[9, 0] = cb_arr[9, 0]
    # flip bottom border's rank names
    cb_arr_flipped[9, 1:9] = np.flip(cb_arr[9, 1:9])
    return cb_arr_flipped


def str_flip(cb_str: str) -> str:
    """Return the chessboard string as flipped string"""
    return(arr2str(arr_flip(str2arr(cb_str))))


def str_isflipped(cb1_str: str, cb2_str: str) -> bool:
    """Return the comparism of 2 chessboards'
       strings, if the 2nd is identical
       but flipped to the 1st"""
    return cb1_str == str_flip(cb2_str)


def arr_isflipped(cb1_arr: np.ndarray, cb2_arr: np.ndarray) -> bool:
    """Return the comparism of 2 chessboards'
       ndarrays, if the 2nd is identical
       but flipped to the 1st"""
    return(np.array_equal(cb1_arr, arr_flip(cb2_arr)))


def isflipped(cb1, cb2) -> bool:
    """Return the comparism of 2 chessboards'
       strings or ndarrays, if the 2nd is identical
       but flipped to the 1st"""
    if np.ndarray == type(cb1):
        cb1_str = arr2str(cb1)
    else:
        cb1_str = cb1
    if np.ndarray == type(cb2):
        cb2_str = arr2str(cb2)
    else:
        cb2_str = cb2
    return str_isflipped(cb1_str, cb2_str)


def str2ttf(cb_str: str) -> str:
    """Return the chessbord string as TTF string"""
    cb_arr = str2arr(cb_str)
    cb_ttf_str = ''
    for x_coord in range(10):
        line = ''
        for y_coord in range(10):
            line += font_dict[cb_arr[x_coord, y_coord]].format('b')
        cb_ttf_str += line + '\n'
    return cb_ttf_str


def arr2ttf(cb_arr: np.ndarray) -> str:
    """Return the chessbord np.ndarray as TTF string"""
    cb_ttf_str = ''
    for x_coord in range(10):
        line = ''
        for y_coord in range(10):
            line += font_dict[str(cb_arr[x_coord, y_coord])].format('b')
        cb_ttf_str += line + '\n'
    return cb_ttf_str


# the chessboard from Black view - as str
START_BLACK_STR = str_flip(START_WHITE_STR)

# the chessboard from White view; as np.ndarray
START_WHITE_ARR = str2arr(START_WHITE_STR)

# the chessboard from Black view - as np.ndarray
START_BLACK_ARR = arr_flip(START_WHITE_ARR)


def _empty_white_cb_arr() -> np.ndarray:
    out = '-w -b -w -b -w -b -w -b \n' + \
          '-b -w -b -w -b -w -b -w \n' + \
          '-w -b -w -b -w -b -w -b \n' + \
          '-b -w -b -w -b -w -b -w \n' + \
          '-w -b -w -b -w -b -w -b \n' + \
          '-b -w -b -w -b -w -b -w \n' + \
          '-w -b -w -b -w -b -w -b \n' + \
          '-b -w -b -w -b -w -b -w \n'
    # make a string
    bw_tmp = str(out).replace('\n', '', -1).replace(' ', '', -1)  # -1 == all
    # make an ndarray
    bw_arr = np.array([bw_tmp[i:i+2]
                       for i in range(0, len(bw_tmp), 2)]).reshape((8, 8))
    cb_arr = START_WHITE_ARR.copy()
    # put into standard white board --> drop pieces
    cb_arr[1:9, 1:9] = bw_arr[0:8, 0:8]
    # return the white board without the pieces
    return cb_arr


EMPTY_WHITE_ARR = _empty_white_cb_arr()

EMPTY_BLACK_ARR = arr_flip(EMPTY_WHITE_ARR)

EMPTY_WHITE_STR = arr2str(EMPTY_WHITE_ARR)

EMPTY_BLACK_STR = arr2str(EMPTY_BLACK_ARR)


def board2arr(board: chess.Board) -> np.ndarray:
    """Return the chessboard ndarray from a 'chess.board'"""
    # the chessboard from White view
    # with
    #   ranks: 8 7 6 5 4 3 2 1
    #   files: a b c d e f g h
    # major part taken from 'chess svg', see:
    #   https://python-chess.readthedocs.io/en/latest/_modules/chess/svg.html#board
    # and adapted to the x,y-array where
    # a (10, 10) board == squares + its borders
    # this chessboard from white view is with
    #   ( 0,  0) top left, and
    #   (10, 10) bottom right

    # as PGN printouts are usually from white perspective
    # this is a reasonable assumption
    orientation = chess.WHITE
    board_arr = np.full((8, 8), '_')
    for square, _ in enumerate(chess.BB_SQUARES):
        # a1 b1 c1 ... h1,
        # a2 b2 c2 ... h2,
        # ...,
        # a8 b8 c8 ... h8
        file_index = chess.square_file(square)
        rank_index = chess.square_rank(square)

        x_coord = (7 - rank_index if orientation else rank_index)
        y_coord = (file_index if orientation else 7 - file_index)

        piece_char = ""
        if board is not None:
            piece = board.piece_at(square)
            if piece:
                piece_char = piece.symbol()
                if chess.WHITE == chess.COLOR_NAMES[piece.color]:
                    piece_char = piece_char.upper()
                board_arr[x_coord, y_coord] = piece_char

    # print(board_arr)
    out_arr = (EMPTY_WHITE_ARR).tolist()
    # print(out_arr)
    # put into an empty board
    for rank in range(8):
        for file in range(8):
            if '_' != board_arr[rank][file]:
                out = str(out_arr[rank+1][file+1]).replace( \
                    '-', str(board_arr[rank][file]))
                out_arr[rank+1][file+1] = out
    return np.array(out_arr)


def board2str(board: chess.Board) -> str:
    """Return the chessboard str from a 'chess.board'"""
    return(arr2str(board2arr(board)))


def board2ttf(board: chess.Board) -> str:
    """Return the chessboard TTF from a 'chess.board'"""
    return(str2ttf(arr2str(board2arr(board))))


def main():
    """some test for the chessboard.py"""
    # some examples
    print('\nChessboard - White')
    print(START_WHITE_STR)

    print('Chessboard - White - flipped')
    print(str_flip(START_WHITE_STR))

    print('isflipped(Chessboard - White, Chessboard - White - flipped):',
          isflipped(START_WHITE_STR, START_BLACK_STR))

    print('\n-------------------------------------')
    print('Chessboard - White - TTF')
    print(str2ttf(START_WHITE_STR))

    print('Chessboard - Black - TTF')
    print(str2ttf(START_BLACK_STR))

    print('-------------------------------------')
    print('Chessboard - White - chess.Board')
    print(board2str(chess.Board()))

    print('Chessboard - White - FEN')
    print('FEN: r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4')
    board = chess.Board(
        'r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4')
    print(board2str(board))

    print('Chessboard - White - FEN --> TTF')
    print(board2ttf(board))


if __name__ == '__main__':
    main()
