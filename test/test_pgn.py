# pylint: disable=invalid-name
"""Functions concerning pgn checks and docx generation"""
import unittest

from context import pgn


class Test_unittest(unittest.TestCase):
    """Collection of tests for pgn module"""
    # Test 1
    def test_get_pgnfile_names_from_dir(self):
        """Checks existance of at least one pgn-file in pgn-dir"""
        # there should be at least on file with extension '.pgn' at directory 'PGN/TEST'
        self.assertEqual(True, len(pgn.get_pgnfile_names_from_dir(pgn_dir='pgn', ext='.pgn')) > 0)

    # Test 2
    def test_get_games_from_pgnfile(self):
        """Checks the pgn game retrieval from a pgn file"""
        # 'PGN/TEST/test_do_not_change.pgn' should contain 5 PGN games
        self.assertEqual(True,
                         len(pgn.get_games_from_pgnfile(\
                             'test/pgn/test_do_not_change.pgn')) == 5)

    # Test 3
    def test_get_incremented_filename(self):
        """Checks generation of incremented filename if already exists"""
        # existing file 'docx_test_datatest_do_not_change' shall not be overwriten,
        # but a new file with incremented numbering shall be chosen as the new
        # file name; for the test: 'docx_test_data/test_do_not_change-1'
        self.assertEqual(True,
                         pgn.get_incremented_filename(\
                             'test/docx/test_do_not_change') == \
                         'test/docx/test_do_not_change-1')

    # Test 4
    def test_prep_ttfboards_from_pgn(self):
        """Test with given pgn move the correct ttfboard genration"""
        # 1. e4
        w_test_brd_str = \
            '1222222223\n' + \
            'ÇtMvWlVmT5\n' + \
            'ÆOoOoOoOo5\n' + \
            'Å*+*+*+*+5\n' + \
            'Ä+*+*+*+*5\n' + \
            'Ã*+*+p+*+5\n' + \
            'Â+*+*+*+*5\n' + \
            'ÁpPpP*PpP5\n' + \
            'ÀRnBqKbNr5\n' + \
            '7ÈÉÊËÌÍÎÏ9\n'
        # 1. e4 e5
        b_test_brd_str = \
            '1222222223\n' + \
            'ÇtMvWlVmT5\n' + \
            'ÆOoOo+oOo5\n' + \
            'Å*+*+*+*+5\n' + \
            'Ä+*+*O*+*5\n' + \
            'Ã*+*+p+*+5\n' + \
            'Â+*+*+*+*5\n' + \
            'ÁpPpP*PpP5\n' + \
            'ÀRnBqKbNr5\n' + \
            '7ÈÉÊËÌÍÎÏ9\n'
        res_dict = pgn.prep_ttfboards_from_pgn('1. e4 e5').iloc[0].to_dict()
        self.assertEqual(True,
                         w_test_brd_str == \
                            res_dict['w_board_ttf'] \
                         and \
                         b_test_brd_str == \
                            res_dict['b_board_ttf'])

    # # Test 5
    # TODO
    # def test_gen_document_from_game(self):
    #     self.assertEqual(True, pgn.gen_document_from_game( params ))

    # # Test 6
    # TODO
    # def test_store_document(self):
    #     self.assertEqual(True, pgn.store_document( params ))

if __name__ == '__main__':
    unittest.main()
