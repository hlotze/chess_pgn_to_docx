# pylint: disable=import-error
"""functions for the eco mgmt of chess games"""

import io
import sys
import os
import os.path

import chess.pgn
import pandas as pd


# #####################################
# # get the eco.csv
# #   see https://www3.diism.unisi.it/~addabbo/ECO_aperture_scacchi.html
# #
# # as a pd.DataFrame: ECO_DF

# ECO_FILENAME = os.path.dirname(os.path.realpath(__file__))+'/eco.zip'
# if not os.path.isfile(ECO_FILENAME):
#     print(f'file \'{ECO_FILENAME}\' does not exits')
#     sys.exit(1)

# ECO_DF = pd.read_csv(ECO_FILENAME,
#                      sep=',',
#                      header=0,
#                      compression={'method': 'zip'})
# # 'ECO_DF' provides the ECO data
# #####################################

ECO_TEST_DATA_DICT = {
    'eco': 'B05',
    'pgn': '1.e4 Nf6 2.e5 Nd5 3.d4 d6 4.Nf3 Bg4 ' +
    '5.Bc4 e6 6.O-O Nb6 7.Be2 Be7 8.h3 Bh5 ' +
    '9.Bf4 Nc6 10.c3 O-O 11.Nbd2 d5 12.b4 a5 ' +
    '13.a3 Qd7 14.Qc2 Bg6 15.Bd3 Rfc8 16.Rfb1 Bf8 ' +
    '17.h4 Ne7 18.g3 Qa4 19.Ne1 Qxc2 ' +
    '20.Bxc2 Bxc2 21.Nxc2 Na4 22.Rb3 b6 23.Kf1 c5 ' +
    '24.bxc5 bxc5 25.dxc5 Rxc5 26.Nb1 Rac8 27.Be3 Rc4 ' +
    '28.Bd4 Nc6 29.Rb5 Nxd4 30.Nxd4 Nxc3 31.Nxc3 ' +
    'Rxd4 32.Ne2 Ra4 33.Ke1 Rxa3 34.Rab1 Bb4+ 35.Kf1 Rd3  0-1'}


#####################################
# new eco procedure
#####################################

NEW_ECO_FILENAME = os.path.dirname(os.path.realpath(__file__))+'/eco.csv'
if not os.path.isfile(NEW_ECO_FILENAME):
    print(f'file \'{NEW_ECO_FILENAME}\' does not exits')
    sys.exit(1)

NEW_ECO_DF = pd.read_csv(NEW_ECO_FILENAME,
                         sep=',',
                         header=0,
                         usecols=["eco", "title", "pgn",
                                  "last_ply",
                                  "sq_from", "sq_to", "sq_check",
                                  "fen"])


def new_get_eco_data_for(eco=None, pgn=None) -> dict:
    """Return the ECO data for the given ECO and PGN, even if ECO is wrong or missing"""
    if eco is None:
        eco = ''
    if pgn is None:
        sys.exit("error: no pgn given at 'get_eco_data_for()'")

    # normalize the pgn string
    pgn = normalize_pgn_string(pgn)

    found_eco_dict = {}
    # do we have an ECO code
    if eco != '':
        # get all entries from pgn.eco_df
        # that fits to given eco_code
        filtered_eco_data_df = NEW_ECO_DF[eco == NEW_ECO_DF['eco']]  # .copy()
        rev_sorted_eco_data_df = filtered_eco_data_df.sort_values(
            'pgn', ascending=False)  # .copy()
        for _, row in rev_sorted_eco_data_df.iterrows():
            #print('len:', len(row['pgn']), '[',row['pgn'], '] last char:', row['pgn'][-1])
            if row['pgn'] == pgn[:len(row['pgn'])]:
                found_eco_dict = row.to_dict()
                break

    # if no ECO available or given ECO is wrong
    # and no related ECO data found
    # do it again and check with complete database
    if not bool(found_eco_dict):
        eco_data_df = NEW_ECO_DF  # .copy()
        rev_sorted_eco_data_df = eco_data_df.sort_values(
            'pgn', ascending=False)  # .copy()
        for _, row in rev_sorted_eco_data_df.iterrows():
            #print('len:', len(row['pgn']), '[',row['pgn'], '] last char:', row['pgn'][-1])
            if row['pgn'] == pgn[:len(row['pgn'])]:
                found_eco_dict = row.to_dict()
                break
    return found_eco_dict


def normalize_pgn_string(pgn: str) -> str:
    """Return a normalized pgn string, e.g.
    '1.g4 d5 2.Bg2 c6' will be normalized to
    '1. g4 d5 2. Bg2 c6'"""
    game = chess.pgn.read_game(io.StringIO(pgn))
    normed_pgn_str = game.board().variation_san(game.mainline_moves())
    if len(game.errors) > 0:
        print(pgn)
    return normed_pgn_str


def main():
    """some test for the eco.py"""
    print('test data')
    print(ECO_TEST_DATA_DICT)

    print('normalized PGN')
    print(normalize_pgn_string(ECO_TEST_DATA_DICT['pgn']))

    # print('complete ECO data for that PGN')
    # res_dict = get_eco_data_for(eco=ECO_TEST_DATA_DICT['eco'], pgn=ECO_TEST_DATA_DICT['pgn'])
    # print(res_dict)

    print('\nNEW complete ECO data for that PGN')
    res_dict = new_get_eco_data_for(
        eco=ECO_TEST_DATA_DICT['eco'], pgn=ECO_TEST_DATA_DICT['pgn'])
    print(res_dict)


if __name__ == '__main__':
    main()
