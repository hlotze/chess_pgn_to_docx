"""Functions concerning pgn checks and docx generation"""
import unittest

from context import pgn




class Test_unittest(unittest.TestCase):

    # Test 1
    # def test_get_pgnfile_names_from_dir(self):
    #     # there should be at least on file with extension '.pgn' at directory 'PGN/TEST'
    #     self.assertEqual(True, 0 < len(pgn.get_pgnfile_names_from_dir(pgn_dir='PGN/TEST', ext='.pgn')))

    # Test 2
    def test_get_games_from_pgnfile(self):
        # 'PGN/TEST/test_do_not_change.pgn' should contain 5 PGN games
        self.assertEqual(True, len(pgn.get_games_from_pgnfile('test/pgn/test_do_not_change.pgn')) == 5)

    # Test 3
    def test_get_incremented_filename(self):
        # existing file 'docx_test_datatest_do_not_change' shall not be overwriten,
        # but a new file with incremented numbering shall be chosen as the new 
        # file name; for the test: 'docx_test_data/test_do_not_change-1'
        self.assertEqual(True, pgn.get_incremented_filename('test/docx/test_do_not_change') == 'test/docx/test_do_not_change-1')
        
    # Test 4
    def test_prep_ttfboards_from_pgn(self):
        # 1. e4
        #                 file         abcdefgh    abcdefgh    abcdefgh    abcdefgh    abcdefgh    abcdefgh    abcdefgh    abcdefgh
        #                 top border  | rank 8 |  | rank 7 |  | rank 6 |  | rank 5 |  | rank 4 |  | rank 3 |  | rank 2 |  | rank 1 |  bottom border
        w_test_brd_str = '1222222223\nÇtMvWlVmT5\nÆOoOoOoOo5\nÅ*+*+*+*+5\nÄ+*+*+*+*5\nÃ*+*+p+*+5\nÂ+*+*+*+*5\nÁpPpP*PpP5\nÀRnBqKbNr5\n7ÈÉÊËÌÍÎÏ9\n'
        # 1. e4 e5                                     |                       |           |                       |
        b_test_brd_str = '1222222223\nÇtMvWlVmT5\nÆOoOo+oOo5\nÅ*+*+*+*+5\nÄ+*+*O*+*5\nÃ*+*+p+*+5\nÂ+*+*+*+*5\nÁpPpP*PpP5\nÀRnBqKbNr5\n7ÈÉÊËÌÍÎÏ9\n'
        res_dict = pgn.prep_ttfboards_from_pgn('1. e4 e5').iloc[0].to_dict()
        self.assertEqual(True, w_test_brd_str == res_dict['w_board_ttf'] and b_test_brd_str == res_dict['b_board_ttf'])

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
