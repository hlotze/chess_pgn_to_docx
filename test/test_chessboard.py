# pylint: disable=too-many-public-methods
# pylint: disable=import-error
"""Functions related to the chessboard"""

import unittest

import chess
import numpy as np

from context import chessboard as cb


class TestChessboard(unittest.TestCase):
    """Collection of tests for chessboard module"""
    # Test 1
    def test_TTF_DICT(self):
        """correctness of names TTF_DICT"""
        self.assertEqual(cb.TTF_DICT, \
                         {'Chess Condal': 'CONDFONT.TTF',
                          'Chess Kingdom': 'KINGFONT.TTF',
                          'Chess Leipzig': 'LEIPFONT.TTF',
                          'Chess Merida': 'MERIFONT.TTF'})

    # Test 2
    def test_font_dict(self):
        """correctness of mapping FONT_DICT"""
        self.assertEqual(cb.FONT_DICT, \
                         {'-w': '*', 'ow': '.', 'xw': 'x',
                          'Kw': 'k', 'Qw': 'q', 'Rw': 'r',
                          'Bw': 'b', 'Nw': 'n', 'Pw': 'p',
                          'kw': 'l', 'qw': 'w', 'rw': 't',
                          'bw': 'v', 'nw': 'm', 'pw': 'o',
                          '-b': '+', 'ob': ':', 'xb': 'X',
                          'Kb': 'K', 'Qb': 'Q', 'Rb': 'R',
                          'Bb': 'B', 'Nb': 'N', 'Pb': 'P',
                          'kb': 'L', 'qb': 'W', 'rb': 'T',
                          'bb': 'V', 'nb': 'M', 'pb': 'O',
                          'fk': '¢', 'fq': '£', 'fr': '¦',
                          'fb': '¥', 'fn': '¤', 'fp': '§',
                          'tl': '1', 'tr': '3', 'bl': '7',
                          'br': '9', '--': '2', '||': '5',
                          '|x': '%', 'a-': 'È', 'b-': 'É',
                          'c-': 'Ê', 'd-': 'Ë', 'e-': 'Ì',
                          'f-': 'Í', 'g-': 'Î', 'h-': 'Ï',
                          '1|': 'À', '2|': 'Á', '3|': 'Â',
                          '4|': 'Ã', '5|': 'Ä', '6|': 'Å',
                          '7|': 'Æ', '8|': 'Ç'})

    # Test 3
    def test_start_white_str(self):
        """correctness of board str from white"""
        self.assertEqual(cb.START_WHITE_STR,
                         'tl -- -- -- -- -- -- -- -- tr \n' +
                         '8| rw nb bw qb kw bb nw rb || \n' +
                         '7| pb pw pb pw pb pw pb pw || \n' +
                         '6| -w -b -w -b -w -b -w -b || \n' +
                         '5| -b -w -b -w -b -w -b -w || \n' +
                         '4| -w -b -w -b -w -b -w -b || \n' +
                         '3| -b -w -b -w -b -w -b -w || \n' +
                         '2| Pw Pb Pw Pb Pw Pb Pw Pb || \n' +
                         '1| Rb Nw Bb Qw Kb Bw Nb Rw || \n' +
                         'bl a- b- c- d- e- f- g- h- br \n')

    # Test 4
    def test_start_black_str(self):
        """correctness of board str from black"""
        self.assertEqual(cb.START_BLACK_STR,
                         'tl -- -- -- -- -- -- -- -- tr \n' +
                         '1| Rw Nb Bw Kb Qw Bb Nw Rb || \n' +
                         '2| Pb Pw Pb Pw Pb Pw Pb Pw || \n' +
                         '3| -w -b -w -b -w -b -w -b || \n' +
                         '4| -b -w -b -w -b -w -b -w || \n' +
                         '5| -w -b -w -b -w -b -w -b || \n' +
                         '6| -b -w -b -w -b -w -b -w || \n' +
                         '7| pw pb pw pb pw pb pw pb || \n' +
                         '8| rb nw bb kw qb bw nb rw || \n' +
                         'bl h- g- f- e- d- c- b- a- br \n')

    # Test 5
    def test_empty_white_str(self):
        """correctness of empty board str from white"""
        self.assertEqual(cb.EMPTY_WHITE_STR,
                         'tl -- -- -- -- -- -- -- -- tr \n' +
                         '8| -w -b -w -b -w -b -w -b || \n' +
                         '7| -b -w -b -w -b -w -b -w || \n' +
                         '6| -w -b -w -b -w -b -w -b || \n' +
                         '5| -b -w -b -w -b -w -b -w || \n' +
                         '4| -w -b -w -b -w -b -w -b || \n' +
                         '3| -b -w -b -w -b -w -b -w || \n' +
                         '2| -w -b -w -b -w -b -w -b || \n' +
                         '1| -b -w -b -w -b -w -b -w || \n' +
                         'bl a- b- c- d- e- f- g- h- br \n')

    # Test 6
    def test_empty_black_str(self):
        """correctness of empty board str from black"""
        self.assertEqual(cb.EMPTY_BLACK_STR,
                         'tl -- -- -- -- -- -- -- -- tr \n' +
                         '1| -w -b -w -b -w -b -w -b || \n' +
                         '2| -b -w -b -w -b -w -b -w || \n' +
                         '3| -w -b -w -b -w -b -w -b || \n' +
                         '4| -b -w -b -w -b -w -b -w || \n' +
                         '5| -w -b -w -b -w -b -w -b || \n' +
                         '6| -b -w -b -w -b -w -b -w || \n' +
                         '7| -w -b -w -b -w -b -w -b || \n' +
                         '8| -b -w -b -w -b -w -b -w || \n' +
                         'bl h- g- f- e- d- c- b- a- br \n')

    # Test 7
    def test_start_white_arr(self):
        """correctness of board array from white"""
        self.assertTrue(
            np.array_equal(cb.START_WHITE_ARR,
                           cb.str2arr(cb.START_WHITE_STR)))

    # Test 8
    def test_start_black_arr(self):
        """correctness of board array from black"""
        self.assertTrue(
            np.array_equal(cb.START_BLACK_ARR,
                           cb.str2arr(cb.START_BLACK_STR)))

    # Test 9
    def test_empty_white_arr(self):
        """correctness of empty board array from white"""
        self.assertTrue(
            np.array_equal(cb.EMPTY_WHITE_ARR,
                           cb.str2arr(cb.EMPTY_WHITE_STR)))

    # Test 10
    def test_empty_black_arr(self):
        """correctness of empty board array from black"""
        self.assertEqual(
            cb.arr2str(cb.EMPTY_BLACK_ARR),
            cb.EMPTY_BLACK_STR)

    # Test 11
    def test_str2arr(self):
        """tests str2arr conversion function"""
        self.assertEqual(
            cb.arr2str(cb.str2arr(cb.START_BLACK_STR)),
            cb.START_BLACK_STR)

    # Test 12
    def test_arr2str(self):
        """tests arr2str conversion function"""
        self.assertEqual(
            cb.arr2str(cb.START_WHITE_ARR),
            cb.START_WHITE_STR)

    # Test 13
    def test_arr_flip(self):
        """tests arr_flip funtion"""
        self.assertTrue(
            np.array_equal(cb.START_BLACK_ARR,
                           cb.arr_flip(cb.START_WHITE_ARR)))

    # Test 14
    def test_str_flip(self):
        """tests str_flip funtion"""
        self.assertEqual(
            cb.START_WHITE_STR,
            cb.str_flip(cb.START_BLACK_STR))

    # Test 15
    def test_str_isflipped(self):
        """check str_isflipped testing if a chessboard ist just the same,
        but flipped from white to black view site"""
        self.assertTrue(
            cb.str_isflipped(cb.START_WHITE_STR,
                             cb.START_BLACK_STR))

    # Test 16
    def test_arr_isflipped(self):
        """check arr_isflipped testing if a chessboard ist just the same,
        but flipped from white to black view site"""
        self.assertTrue(
            cb.arr_isflipped(cb.START_WHITE_ARR,
                             cb.START_BLACK_ARR))

    # Test 17
    def test_isflipped(self):
        """check isflipped testing if a chessboard ist just the same,
        but flipped from white to black view site"""
        self.assertTrue(
            cb.isflipped(cb.START_WHITE_ARR,
                         cb.START_BLACK_STR))

    # Test 18
    def test_str2ttf(self):
        """test str2ttf function"""
        self.assertEqual(
            cb.str2ttf(cb.START_WHITE_STR),
            '1222222223\n' +
            'ÇtMvWlVmT5\n' +
            'ÆOoOoOoOo5\n' +
            'Å*+*+*+*+5\n' +
            'Ä+*+*+*+*5\n' +
            'Ã*+*+*+*+5\n' +
            'Â+*+*+*+*5\n' +
            'ÁpPpPpPpP5\n' +
            'ÀRnBqKbNr5\n' +
            '7ÈÉÊËÌÍÎÏ9\n')

    # Test 19
    def test_arr2ttf(self):
        """test arr2ttf function"""
        self.assertEqual(
            cb.arr2ttf(cb.START_WHITE_ARR),
            '1222222223\n' +
            'ÇtMvWlVmT5\n' +
            'ÆOoOoOoOo5\n' +
            'Å*+*+*+*+5\n' +
            'Ä+*+*+*+*5\n' +
            'Ã*+*+*+*+5\n' +
            'Â+*+*+*+*5\n' +
            'ÁpPpPpPpP5\n' +
            'ÀRnBqKbNr5\n' +
            '7ÈÉÊËÌÍÎÏ9\n')

    # Test 20
    def test_board2arr(self):
        """test board2arr function"""
        self.assertEqual(
            cb.arr2str(cb.board2arr(chess.Board())),
            cb.START_WHITE_STR)

    # Test 21
    def test_board2str(self):
        """test board2str function"""
        self.assertEqual(
            cb.board2str(chess.Board()),
            cb.START_WHITE_STR)

    # Test 22
    def test_board2ttf(self):
        """test board2ttf function"""
        self.assertEqual(
            cb.board2ttf(chess.Board()),
            cb.str2ttf(cb.START_WHITE_STR))

    # Test 23
    def test_get_linear_pos_e2(self):
        """test find linear pos for from e2"""
        self.assertEqual(
            cb.get_linear_pos('e2'), 82)

    # Test 24
    def test_get_linear_pos_e4(self):
        """test find linear pos for to e4"""
        self.assertEqual(
            cb.get_linear_pos('e4'), 60)

    # Test 25
    def test_divide_ttf_str_2_marks(self):
        """test partitioning the ttf str"""
        # make a chess.board
        board = chess.Board()
        # with a move
        board.push_san("e4")
        # partition the ttf of the board
        ttf_parts_df = cb.divide_ttf_str(cb.board2ttf(board), '', 'e2', 'e4')
        # put parts together for comparism
        ttf_str = ''
        for _, ttf_part in enumerate(ttf_parts_df['part']):
            ttf_str += ttf_part
        self.assertEqual(
            cb.board2ttf(board), ttf_str)

    # Test 26
    def test_divide_ttf_str_3_mark(self):
        """test partitioning the ttf str"""
        # make a chess.board
        board = chess.Board('6R1/8/8/7k/2K5/8/8/6R1 w - - 0 1')
        # with a move
        board.push_san("Rh1")
        # partition the ttf of the board
        ttf_parts_df = cb.divide_ttf_str(cb.board2ttf(board), 'h5', 'g1', 'h1')
        #print(ttf_parts_df)
        # put parts together for comparism
        ttf_str = ''
        for _, ttf_part in enumerate(ttf_parts_df['part']):
            ttf_str += ttf_part
        self.assertEqual(
            cb.board2ttf(board), ttf_str)

if __name__ == '__main__':
    unittest.main()
