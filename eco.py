import copy
import io

import chess.pgn
import pandas as pd

#####################################
# get the eco.csv
#   see https://www3.diism.unisi.it/~addabbo/ECO_aperture_scacchi.html
#
# as a pd.DataFrame: eco_df
try:
    # check if file exists
    f = open('eco.csv', 'r')
    f.close

    eco_df = pd.read_csv('eco.csv',
                        sep=',',
                        header=0)

except IOError:
    print("File not accessible: ", 'eco.csv')

finally:
    f.close()

# 'eco_df' provides the ECO data
#####################################

eco_test_data_dict = {
    'eco' : 'B05',
    'pgn' : '1.e4 Nf6 2.e5 Nd5 3.d4 d6 4.Nf3 Bg4 ' + \
            '5.Bc4 e6 6.O-O Nb6 7.Be2 Be7 8.h3 Bh5 ' + \
            '9.Bf4 Nc6 10.c3 O-O 11.Nbd2 d5 12.b4 a5 ' + \
            '13.a3 Qd7 14.Qc2 Bg6 15.Bd3 Rfc8 16.Rfb1 Bf8 ' + \
            '17.h4 Ne7 18.g3 Qa4 19.Ne1 Qxc2 ' + \
            '20.Bxc2 Bxc2 21.Nxc2 Na4 22.Rb3 b6 23.Kf1 c5 ' + \
            '24.bxc5 bxc5 25.dxc5 Rxc5 26.Nb1 Rac8 27.Be3 Rc4 '+ \
            '28.Bd4 Nc6 29.Rb5 Nxd4 30.Nxd4 Nxc3 31.Nxc3 ' + \
            'Rxd4 32.Ne2 Ra4 33.Ke1 Rxa3 34.Rab1 Bb4+ 35.Kf1 Rd3  0-1'}

def normalize_pgn_string(pgn:str) -> str:
    """Return form a pgn string a normalized pgn string, e.g. '1.g4 d5 2.Bg2 c6' will be normalized to '1. g4 d5 2. Bg2 c6'"""
    game = chess.pgn.read_game(io.StringIO(pgn))
    normed_pgn_str = game.board().variation_san(game.mainline_moves())
    return(normed_pgn_str)

def get_eco_data_for(eco='', pgn='') -> dict:
    # normalize the pgn string
    pgn = normalize_pgn_string(pgn)

    # do we have a eco code
    if '' != eco:
        # get all entries from pgn.eco_df
        # that fits to given eco_code
        eco_data_df = eco_df[eco == eco_df['eco']].copy()
    else:
        eco_data_df = eco_df.copy()

    res_df = eco_data_df.sort_values('pgn', ascending=False).copy()
    eco_dict = {}
    for index, row in res_df.iterrows():
        #print('len:', len(row['pgn']), '[',row['pgn'], '] last char:', row['pgn'][-1])
        if row['pgn'] == pgn[:len(row['pgn'])]:
            eco_dict = row.to_dict()
            break

    if not bool(eco_dict):
        # no eco found, e.g. if wrong ECO from PGN was given
        # again check game's pgn against the complete eco data
        eco_data_df = eco_df.copy()
        res_df = eco_data_df.sort_values('pgn', ascending=False).copy()
        for index, row in res_df.iterrows():
            #print('len:', len(row['pgn']), '[',row['pgn'], '] last char:', row['pgn'][-1])
            if row['pgn'] == pgn[:len(row['pgn'])]:
                eco_dict = row.to_dict()
                break

    return(eco_dict)

def main():

    print('test data')
    print(eco_test_data_dict)

    print('normalized PGN')
    print(normalize_pgn_string(eco_test_data_dict['pgn']))

    print('complete ECO data for that PGN')
    res_dict = get_eco_data_for(eco=eco_test_data_dict['eco'], pgn=eco_test_data_dict['pgn'])
    print(res_dict)

if __name__ == '__main__':
    main()