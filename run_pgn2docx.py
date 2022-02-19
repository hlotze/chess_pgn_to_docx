"""generates the docx form given pgn by usage of module pgn2docx"""

import os.path
import sys
#import numpy as np
#import pandas as pd
#from docx import Document
#from docx.enum.text import WD_LINE_SPACING, WD_PARAGRAPH_ALIGNMENT
#from docx.oxml import OxmlElement, ns
#from docx.shared import Inches, Mm, Pt

import eco
import pgn


def main():
    """Return the genrated docx"""
    ##################################################
    # for development just use
    #   'PGN/TEST/test_do_not_change.pgn' with 5 games
    # and only its last pgn to generate one document
    # with the diagrams, at
    #   'DOCX/TEST'
    # (you have to run this 'pgn.py')
    ##################################################
    pgn_dir = 'PGN'
    if not os.path.isdir(pgn_dir):
        print(f'directory \'{pgn_dir}\' does not exits, please create it.')
        sys.exit(1)
    file_names_list = pgn.get_pgnfile_names_from_dir(pgn_dir=pgn_dir)

    for fname in file_names_list:
        try:
            # check if file exists
            file_obj = open(fname, 'r')
            file_obj.close()

            # start to get the games out of one pgn file
            games_df = pgn.get_games_from_pgnfile(fname)

            for index in range(len(games_df)):
                one_game_dict = games_df.iloc[index].to_dict()

                eco_result_dict = {}
                if 'ECO' in one_game_dict.keys():
                    eco_result_dict = eco.get_eco_data_for(eco=one_game_dict['ECO'],
                                                           pgn=one_game_dict['pgn'])
                else:
                    eco_result_dict = eco.get_eco_data_for(eco='',
                                                           pgn=one_game_dict['pgn'])

                my_doc = pgn.gen_document_from_game(one_game_dict,
                                                    eco_result_dict,
                                                    ttf_font_name='Chess Merida')

                # fn fix for lichess pgn files
                event = one_game_dict['Event'].replace(
                    '/', '_').replace(':', '_').replace('.', '-')
                site = one_game_dict['Site'].replace(
                    '/', '_').replace(':', '_').replace('.', '-')

                docx_fn = 'DOCX/' + one_game_dict['Date'].replace('.', '-') + '_' + \
                    event + '_' + \
                    site + '_( ' + \
                    one_game_dict['White'] + ' - ' + \
                    one_game_dict['Black'] + ' ).docx'
                docx_fn = docx_fn.replace('??', '_')

                ret_dict = pgn.store_document(my_doc, docx_fn)
                print('stored:', ret_dict['file_name'])

        except IOError:
            print("File not accessible: ", fname)
        finally:
            file_obj.close()


if __name__ == '__main__':
    main()
