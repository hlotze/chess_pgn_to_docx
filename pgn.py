import codecs
import io
import os
import re
import sys
from pathlib import Path

import chess
import chess.pgn
import numpy as np
import pandas as pd
from docx import Document

import chessboard as cb

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

def prep_ttfboards_from_pgn(pgn_str: str) -> pd.DataFrame:
    """Return at each row full move info: W & B SAN string and W & B TTF board string"""
    # start chess board
    board = chess.Board()
    game = chess.pgn.read_game(io.StringIO(pgn_str))
    
    # prep for half moves
    half_moves_df = pd.DataFrame()
    for move in game.mainline_moves():
        # dict of half move infos
        move_dict = {}
        
        move = chess.Move.from_uci(move.uci())
        move_dict['FMVN'] = int(board.fullmove_number)
        move_dict['SAN'] = board.san(move)

        # TODO fromto for later markup
        move_dict['sq_from'] = move.uci()[:2]
        move_dict['sq_to'] = move.uci()[2:4]
        # site to move chess.WHITE or chess.BLACK
        move_dict['player'] = board.turn
        if chess.WHITE == board.turn:
            move_dict['mv_san_str'] = \
                str(move_dict['FMVN']) + '. ' + \
                move_dict['SAN'] + ' ... '
        else:
            move_dict['mv_san_str'] = \
                str(move_dict['FMVN']) + '. ' + \
                ' ... ' + move_dict['SAN']        
            
        board.push(move)
        sq = ''
        if board.is_check():
            sq = chess.square_name(board.king(board.turn))
        move_dict['sq_check'] = sq
        
        move_dict['board_arr'] = cb.board2arr(board)
        #print(move_dict)
        half_moves_df = half_moves_df.append(move_dict, ignore_index=True)

    half_moves_df = half_moves_df.astype({'FMVN' : np.uint8})
    #print(half_moves_df)
    
    # half moves to full moves data
    # for direct use at document creation
    full_moves_df = pd.DataFrame()
    full_move_dict = {}
    for ix, hmv in half_moves_df.iterrows():
        full_move_dict['FMVN'] = int(hmv['FMVN'])
        if chess.WHITE == hmv['player']:
            full_move_dict['w_hmv_str'] = hmv['mv_san_str']
            # depending on marked squares 
            # change the boards' ttf representation
            full_move_dict['w_sq_from'] = hmv['sq_from']
            full_move_dict['w_sq_to'] = hmv['sq_to']
            full_move_dict['w_sq_check'] = hmv['sq_check']
            full_move_dict['w_board_ttf'] = cb.arr2ttf(hmv['board_arr'])
        else:
            full_move_dict['b_hmv_str'] = full_move_dict['w_hmv_str'][:-5] + ' ' +  hmv['SAN']
            # depending on marked squares 
            # change the boards' ttf representation
            full_move_dict['b_sq_from'] = hmv['sq_from']
            full_move_dict['b_sq_to'] = hmv['sq_to']
            full_move_dict['b_sq_check'] = hmv['sq_check']
            full_move_dict['b_board_arr'] = cb.arr2ttf(hmv['board_arr'])
            full_moves_df = full_moves_df.append(full_move_dict, ignore_index=True)
    full_moves_df = full_moves_df.astype({'FMVN' : np.uint8})
    return(full_moves_df)    


def gen_document_from_game(game_dict: dict)->Document:

    doc = Document()
    
    # just the first page of the booklet
    doc.add_heading('{file}'.format(file=game_dict['file']), 0)
    doc.add_paragraph('Event: {Event} - Site: {Site} - Date: {Date}'.\
        format(Event=game_dict['Event'], \
               Site=game_dict['Site'], \
               Date=game_dict['Date']))
    doc.add_paragraph('{White} vs. {Black}   {Result}'.\
        format(White=game_dict['White'], \
               Black=game_dict['Black'], \
               Result=game_dict['Result']))
    # TODO see https://www3.diism.unisi.it/~addabbo/ECO_aperture_scacchi.html
    if 'ECO' in game_dict.keys():
        doc.add_paragraph('{ECO}'.format(ECO=game_dict['ECO']))
    
    # chess move list
    mv_list = [hm.split(' ') for hm in [mv.rstrip() for mv in re.split('\d*\. ', game_dict['pgn'])[1:]]]
    table = doc.add_table(len(mv_list)+1,3)
    row = table.rows[0]
    row.cells[1].text = game_dict['White']
    row.cells[2].text = game_dict['Black']
    for i in range(len(mv_list)):
        row = table.rows[i+1]
        row.cells[0].text = str(i+1)+'.'
        row.cells[1].text = mv_list[i][0]
        row.cells[2].text = mv_list[i][1]
    doc.add_page_break()

    # now the digrams 4 full move diagrams at each page
    doc.add_table(4,2)



    return(doc)


def get_incremented_filename(filename:str)->str:
    """Return the given filename if exists with an increment"""
    name, ext = os.path.splitext(filename)
    seq = 0
    # continue from existing sequence number if any
    rex = re.search(r"^(.*)-(\d+)$", name)
    if rex:
        name = rex[1]
        seq = int(rex[2])
    
    while os.path.exists(filename):
        seq += 1
        filename = f"{name}-{seq}{ext}"
    return(filename)


def store_document(doc: Document, file_name: str)-> str:
    """Return True after Document is stored with file_name"""
    file_name = get_incremented_filename(file_name)
    doc.save(file_name)
    # check that file name ist stored
    return(os.path.exists(file_name))




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
