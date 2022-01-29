import os
import sys
import unittest

import chess
import numpy as np
import pandas as pd

import pgn as pgn


class Test_unittest(unittest.TestCase):

    # Test 1
    def test_get_pgnfile_names_from_dir(self):
        # there should be at least on file with extension '.pgn' at directory 'PGN/TEST'
        self.assertEqual(True, 0 < len(pgn.get_pgnfile_names_from_dir(dir='PGN/TEST', ext='.pgn')))

    # Test 2
    def test_get_games_from_pgnfile(self):
        # 'PGN/TEST/test_do_not_change.pgn' should contain 5 PGN games
        self.assertEqual(True, 5 == len(pgn.get_games_from_pgnfile('PGN/TEST/test_do_not_change.pgn')))

    # Test 3
    def test_get_incremented_filename(self):
        # existing file 'DOCX/TEST/test_do_not_change' shall not be overwriten,
        # but a new file with incremented numbering shall be chosen as the new 
        # file name; for the test: 'DOCX/TEST/test_do_not_change-1'
        self.assertEqual(True, 'DOCX/TEST/test_do_not_change-1' == pgn.get_incremented_filename('DOCX/TEST/test_do_not_change'))
        

if __name__ == '__main__':
    unittest.main()
