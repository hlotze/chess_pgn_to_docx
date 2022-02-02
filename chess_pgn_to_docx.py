

##################################################
# for development just use
#   'PGN/TEST/test_do_not_change.pgn' with 5 games
# and only its last pgn to generate one document
# with the diagrams, at
#   'DOCX/TEST'
# (you have to run this 'pgn.py')
##################################################

import numpy as np
import pandas as pd
from docx import Document
from docx.enum.text import WD_LINE_SPACING, WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement, ns
from docx.shared import Inches, Mm, Pt

#import chessboard as cb
import pgn as pgn
import eco as eco

file_names_list = pgn.get_pgnfile_names_from_dir(dir='PGN')

for fn in file_names_list:
    try:
        # check if file exists
        f = open(fn, 'r')
        f.close

        # start to get the games out of one pgn file
        games_df = pgn.get_games_from_pgnfile(fn)

        for ix in range(len(games_df)):
            one_game_dict = games_df.iloc[ix].to_dict()

            eco_result_dict = {}
            if 'ECO' in one_game_dict.keys():
                eco_result_dict = eco.get_eco_data_for(eco=one_game_dict['ECO'], pgn=one_game_dict['pgn'])
            else:
                eco_result_dict = eco.get_eco_data_for(eco='', pgn=one_game_dict['pgn'])

            my_doc = pgn.gen_document_from_game(one_game_dict, eco_result_dict)
            
            # fn fix for lichess pgn files
            event = one_game_dict['Event'].replace(
                '/', '_').replace(':', '_').replace('.', '-')
            site = one_game_dict['Site'].replace(
                '/', '_').replace(':', '_').replace('.', '-')
            
            fn = 'DOCX/' + one_game_dict['Date'].replace('.', '-') + '_' + \
                event + '_' + \
                site + '_( ' + \
                one_game_dict['White'] + ' - ' + \
                one_game_dict['Black'] + ' ).docx'
            fn = fn.replace('??', '_')

            ret_dict = pgn.store_document(my_doc, fn)
            print('stored:', ret_dict['file_name'])

    except IOError:
        print("File not accessible: ", fn)
    finally:
        f.close()
