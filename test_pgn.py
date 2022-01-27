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
        self.assertEqual(True, 0 < len(pgn.get_pgnfile_names_from_dir(dir='PGN/TEST', ext='.pgn')))

    # Test 2
    def test_get_games_from_pgnfile(self):
        self.assertEqual(True, 5 == len(pgn.get_games_from_pgnfile('PGN/TEST/test.pgn')))

if __name__ == '__main__':
    unittest.main()
