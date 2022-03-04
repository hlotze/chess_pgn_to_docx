"""Functions related to the eco classification of standard chess"""
import unittest

from context import eco


class TestEco(unittest.TestCase):
    """collections of tests for the eco module"""
    # Test 1

    def test_normalize_pgn_string(self):
        """test the normalization, as given from chess.board,
        of a pgn chess game notation"""
        self.assertEqual('1. e4 Nf6 2. e5 Nd5 3. d4 d6',
                         eco.normalize_pgn_string('1.e4 Nf6 2.e5 Nd5 3.d4 d6'))

    # # Test 2
    # def test_get_eco_data_for__correct_eco(self):
    #     """test the eco classification function of a given eco + pgn"""
    #     res = eco.get_eco_data_for(eco='A01', pgn='1. b3')
    #     self.assertTrue(bool(res['eco'] == 'A01' and res['pgn'] == '1. b3'))

    # # Test 3
    # # find correct classification for
    # # wrong given ECO
    # def test_get_eco_data_for__wrong_eco(self):
    #     """test the eco classification function of a given wrong eco + pgn"""
    #     res = eco.get_eco_data_for(eco='B01', pgn='1. b3')
    #     self.assertTrue(bool(res['eco'] == 'A01' and res['pgn'] == '1. b3'))

    # # Test 4
    # # find correct classification
    # # if only PGN is given
    # def test_get_eco_data_for__pgn_only(self):
    #     """test the eco classification function of a given pgn only"""
    #     res = eco.get_eco_data_for(pgn='1. b3')
    #     self.assertTrue(bool(res['eco'] == 'A01' and res['pgn'] == '1. b3'))

    #######################
    # NEW eco
    #######################
        # Test 2
    def test_new_get_eco_data_for__correct_eco(self):
        """test the eco classification function of a given eco + pgn"""
        res = eco.new_get_eco_data_for(eco='A01', pgn='1. b3')
        self.assertTrue(bool(res['eco'] == 'A01' and res['pgn'] == '1. b3'))

    # Test 3
    # find correct classification for
    # wrong given ECO
    def test_new_get_eco_data_for__wrong_eco(self):
        """test the eco classification function of a given wrong eco + pgn"""
        res = eco.new_get_eco_data_for(eco='B01', pgn='1. b3')
        self.assertTrue(bool(res['eco'] == 'A01' and res['pgn'] == '1. b3'))

    # Test 4
    # find correct classification
    # if only PGN is given
    def test_new_get_eco_data_for__pgn_only(self):
        """test the eco classification function of a given pgn only"""
        res = eco.new_get_eco_data_for(pgn='1. b3')
        self.assertTrue(bool(res['eco'] == 'A01' and res['pgn'] == '1. b3'))


if __name__ == '__main__':
    unittest.main()
