
import unittest

import eco as eco


class Test_unittest(unittest.TestCase):

    # Test 1
    def test_normalize_pgn_string(self):
        self.assertEqual('1. e4 Nf6 2. e5 Nd5 3. d4 d6', 
            eco.normalize_pgn_string('1.e4 Nf6 2.e5 Nd5 3.d4 d6'))

    # Test 2
    def test_get_eco_data_for__correct_eco(self):
        res = eco.get_eco_data_for(eco='A01', pgn='1. b3')
        self.assertEqual(True, bool('A01' == res['eco'] and '1. b3' == res['pgn']))

    # Test 3
    # find correct classification for 
    # wrong given ECO
    def test_get_eco_data_for__wrong_eco(self):
        res = eco.get_eco_data_for(eco='B01', pgn='1. b3')
        self.assertEqual(True, bool('A01' == res['eco'] and '1. b3' == res['pgn']))

    # Test 4
    # find correct classification  
    # if only PGN is given
    def test_get_eco_data_for__pgn_only(self):
        res = eco.get_eco_data_for(pgn='1. b3')
        self.assertEqual(True, bool('A01' == res['eco'] and '1. b3' == res['pgn']))
        
if __name__ == '__main__':
    unittest.main()    
