import codecs
import io
import os
import re
import sys


import chess
import chess.pgn
import numpy as np
import pandas as pd
from docx import Document
from docx.enum.text import WD_LINE_SPACING, WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement, ns
from docx.shared import Pt

import chessboard as cb

#from docx.oxml.ns import nsdecls



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
            #full_move_dict['b_hmv_str'] = full_move_dict['w_hmv_str'][:-5] + ' ' +  hmv['SAN']
            full_move_dict['b_hmv_str'] = hmv['mv_san_str']
            # depending on marked squares 
            # change the boards' ttf representation
            full_move_dict['b_sq_from'] = hmv['sq_from']
            full_move_dict['b_sq_to'] = hmv['sq_to']
            full_move_dict['b_sq_check'] = hmv['sq_check']
            full_move_dict['b_board_ttf'] = cb.arr2ttf(hmv['board_arr'])
            full_moves_df = full_moves_df.append(full_move_dict, ignore_index=True)
    full_moves_df = full_moves_df.astype({'FMVN' : np.uint8})
    return(full_moves_df)    



def gen_document_from_game(game_dict: dict)->Document:

    doc = Document()

    header = doc.sections[0].header

    # header
    head = header.paragraphs[0]
    head.text = '{Date} {Event}, {Site}\n{White} vs. {Black}   {Result}'.\
        format(Event=game_dict['Event'], \
               Site=game_dict['Site'], \
               Date=game_dict['Date'].replace('.','-'), \
               White=game_dict['White'], \
               Black=game_dict['Black'], \
               Result=game_dict['Result'])

    # footer: just the running page number
    def create_element(name):
        return(OxmlElement(name))

    def create_attribute(element, name, value):
        element.set(ns.qn(name), value)

    # taken from
    #   https://stackoverflow.com/questions/56658872/add-page-number-using-python-docx/62534711#62534711
    def add_page_number(paragraph):
        # paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT

        page_run = paragraph.add_run()
        t1 = create_element('w:t')
        create_attribute(t1, 'xml:space', 'preserve')
        t1.text = 'Page '
        page_run._r.append(t1)

        page_num_run = paragraph.add_run()

        fldChar1 = create_element('w:fldChar')
        create_attribute(fldChar1, 'w:fldCharType', 'begin')

        instrText = create_element('w:instrText')
        create_attribute(instrText, 'xml:space', 'preserve')
        instrText.text = "PAGE"

        fldChar2 = create_element('w:fldChar')
        create_attribute(fldChar2, 'w:fldCharType', 'end')

        page_num_run._r.append(fldChar1)
        page_num_run._r.append(instrText)
        page_num_run._r.append(fldChar2)

        of_run = paragraph.add_run()
        t2 = create_element('w:t')
        create_attribute(t2, 'xml:space', 'preserve')
        t2.text = ' of '
        of_run._r.append(t2)

        fldChar3 = create_element('w:fldChar')
        create_attribute(fldChar3, 'w:fldCharType', 'begin')

        instrText2 = create_element('w:instrText')
        create_attribute(instrText2, 'xml:space', 'preserve')
        instrText2.text = "NUMPAGES"

        fldChar4 = create_element('w:fldChar')
        create_attribute(fldChar4, 'w:fldCharType', 'end')

        num_pages_run = paragraph.add_run()
        num_pages_run._r.append(fldChar3)
        num_pages_run._r.append(instrText2)
        num_pages_run._r.append(fldChar4)

    add_page_number(doc.sections[0].footer.paragraphs[0]) #.add_run())
    doc.sections[0].footer.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
    
    # just the first page of the booklet
    #print(game_dict.keys())
    out_str = ''
    for key in game_dict.keys():
        if 'file' != key and 'pgn' != key:
            out_str = out_str + '[{k}] \"{v}\"\n'.format(k=key, v=game_dict[key])
    out_str = out_str + '\n'
    out_str = out_str + '{pgn}  {res}\n'.format(pgn=game_dict['pgn'], res=game_dict['Result'])
    doc.add_paragraph(out_str)

    # doc.add_heading('{file}'.format(file=game_dict['file']), 0)
    # doc.add_paragraph('Event: {Event} - Site: {Site} - Date: {Date}'.\
    #     format(Event=game_dict['Event'], \
    #            Site=game_dict['Site'], \
    #            Date=game_dict['Date']))
    # doc.add_paragraph('{White} vs. {Black}   {Result}'.\
    #     format(White=game_dict['White'], \
    #            Black=game_dict['Black'], \
    #            Result=game_dict['Result']))

    # TODO see https://www3.diism.unisi.it/~addabbo/ECO_aperture_scacchi.html
    if 'ECO' in game_dict.keys():
        doc.add_paragraph('{ECO}'.format(ECO=game_dict['ECO']))
        # some words about the game's ECO
        doc.add_paragraph('some words about the game\'s ECO')
    
    # chess move list - as a table
    # dropped 
    #   just provide the PGN at 1st page 
    #
    # mv_list = [hm.split(' ') for hm in [mv.rstrip() for mv in re.split('\d*\. ', game_dict['pgn'])[1:]]]
    # mv_tbl = doc.add_table(len(mv_list)+1,3)
    # mv_row = mv_tbl.rows[0]
    # mv_row.cells[1].text = game_dict['White']
    # mv_row.cells[2].text = game_dict['Black']
    # for i in range(len(mv_list)):
    #     mv_row = mv_tbl.rows[i+1]
    #     mv_row.cells[0].text = str(i+1)+'.'
    #     mv_row.cells[1].text = mv_list[i][0]
    #     mv_row.cells[2].text = mv_list[i][1]

    doc.add_page_break()

    # the PGN digagrams

    # the PGN data for diagram genration
    boards_df = prep_ttfboards_from_pgn(game_dict['pgn'])
    
    boards_tbl = doc.add_table(2*len(boards_df), 2)
    for ix, fmv in boards_df.iterrows():
        # now the digrams 3 full move diagrams at each page
        #if 0 == ix % 6:
        #    doc.add_page_break()


        brd_row = boards_tbl.rows[2*ix]
        
        # the board diagrams
        brd_row.cells[0].text = fmv['w_board_ttf'][:-1]
        brd_cell_paragraph = brd_row.cells[0].paragraphs[0]
        brd_cell_paragraph.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        brd_cell_paragraph.paragraph_format.keep_with_next = True
        brd_cell_paragraph.paragraph_format.space_before = Pt(0)
        brd_cell_paragraph.paragraph_format.space_after = Pt(0)
        brd_run = brd_cell_paragraph.runs
        brd_fnt = brd_run[0].font
        brd_fnt.name = 'Chess Merida'
        brd_fnt.size = Pt(20)
        brd_row.cells[1].text = fmv['b_board_ttf'][:-1]
        brd_cell_paragraph = brd_row.cells[1].paragraphs[0]
        brd_cell_paragraph.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        brd_cell_paragraph.paragraph_format.keep_with_next = True
        brd_cell_paragraph.paragraph_format.space_before = Pt(0)
        brd_cell_paragraph.paragraph_format.space_after = Pt(0)
        brd_run = brd_cell_paragraph.runs
        brd_fnt = brd_run[0].font
        brd_fnt.name = 'Chess Merida' 
        brd_fnt.size = Pt(20)

        if ix == len(boards_df)-1:
            if 0 == len(fmv['b_hmv_str']):
                fmv['w_hmv_str'] = fmv['w_hmv_str'] + '   ' + game_dict['Result']
            else:
                fmv['b_hmv_str'] = fmv['b_hmv_str'] + '   ' + game_dict['Result']
        # the SAN below the board diagrams
        brd_row = boards_tbl.rows[2*ix+1]
        brd_row.cells[0].text = fmv['w_hmv_str']
        brd_row.cells[0].paragraphs[0].style.font.name = 'Verdana'
        brd_row.cells[0].paragraphs[0].paragraph_format.space_after = Pt(0)
        brd_row.cells[1].text = fmv['b_hmv_str']
        brd_row.cells[1].paragraphs[0].style.font.name = 'Verdana'
        brd_row.cells[1].paragraphs[0].paragraph_format.space_after = Pt(0)



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
    return({'done'      : os.path.exists(file_name),\
            'file_name' : file_name})


def main():

    # for development just use test.pgn with 5 games
    fn = get_pgnfile_names_from_dir(dir='PGN/TEST')[0]

    try:
        # check if file exists
        f = open(fn, 'r')
        f.close

        # start to get the games out of one pgn file
        games_df = get_games_from_pgnfile(fn)

        one_game_dict = games_df.iloc[-1].to_dict()
        #print(one_game_dict)

        my_doc = gen_document_from_game(one_game_dict)

        fn = 'DOCX/TEST/' + one_game_dict['Date'].replace('.','-')  + '_' + \
                            one_game_dict['Event'] + '_' + \
                            one_game_dict['Site']  + '_( ' + \
                            one_game_dict['White'] + ' - ' + \
                            one_game_dict['Black'] + ' ).docx'
        
        # store document
        ret_dict = store_document(my_doc, fn)
        print('stored:', ret_dict['file_name'])

    except IOError:
        print("File not accessible: ", fn)
    finally:
        f.close()

    return()




# def main():
#     # at least one pgn-file should be in this dir
#     print(get_pgnfile_names_from_dir(dir='PGN/TEST'))
    
#     games_df = pd.DataFrame()
#     for fn in get_pgnfile_names_from_dir(dir='PGN/TEST'):
#         games_df = games_df.append(get_games_from_pgnfile(fn))
#         #print(games_df.tail(3))
#     print('\nnow only the last PGN game as dict:')
#     print(games_df.iloc[-1].to_dict())
#     return()

if __name__ == '__main__':
    main()
