import codecs
import os
import sys

import chess
import chess.pgn
import numpy as np
import pandas as pd
from docx import Document


def get_pgnfile_names_from_dir(dir='PGN', ext='.pgn')->list:
    ### Return a python list with filenames from a given directory and given extension '.pgn' '.PGN' ### 
    file_names_list = []
    for file in os.listdir(dir):
        if file.endswith(ext) or file.endswith(ext.upper()):
            if os.path.isfile(os.path.join(dir, file)):
                file_names_list.append(os.path.join(dir, file))
    return(sorted(file_names_list))


def get_games_from_pgnfile(file_name:str)->pd.DataFrame:
    """Return a DataFrame with all games of the file_name, incl. headers and pgn game notation."""
    # existance of file is ensured
    pgn = open(file_name, encoding="utf-8")
    games_df = pd.DataFrame()
    # iterate over all games of a file
    while True:
        game = chess.pgn.read_game(pgn)
        if game is None:
            break

        game_dict = dict(game.headers)
        game_dict["pgn"] = game.board().variation_san(game.mainline_moves())
        game_dict['file'] = file_name
        games_df = games_df.append(game_dict, ignore_index=True)
    return(games_df)

def gen_document_from_game(game_dict: dict)->Document:

    return()

def store_document(file_name: str)->bool:

    return()




def main():
    
    # at least one pgn-file should be in this dir
    print(get_pgnfile_names_from_dir(dir='PGN/TEST'))
    
    games_df = pd.DataFrame()
    for fn in get_pgnfile_names_from_dir(dir='PGN/TEST'):
        games_df = games_df.append(get_games_from_pgnfile(fn))
        #print(games_df.tail(3))
    print('\nnow only the last PGN game as dict:')
    print(games_df.iloc[-1].to_dict())
    
    
    return()

if __name__ == '__main__':
    main()
