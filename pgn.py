#import codecs
import io
import os
import re
import warnings

import chess
import chess.pgn
import numpy as np

warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
from docx import Document
from docx.enum.text import WD_LINE_SPACING, WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement, ns
from docx.shared import Inches, Mm, Pt

import chessboard as cb
import eco as eco


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
    pgn = open(file_name)#, encoding="utf-8")
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


def gen_document_from_game(game_dict: dict, eco_dict: dict)->Document:
    """Return a docx.Document Din A4 with the chess diagrams for a given game_dict"""
    doc = Document()

    #  set to A4 --------------------------------------
    # see
    #   https://stackoverflow.com/questions/43724030/how-to-change-page-size-to-a4-in-python-docx
    section = doc.sections[0]
    section.page_height = Mm(297)
    section.page_width = Mm(210)
    section.left_margin = Mm(30)
    section.right_margin = Mm(25)
    section.top_margin = Mm(30)
    section.bottom_margin = Mm(15)
    section.header_distance = Mm(15)
    section.footer_distance = Mm(10)
    #  set to A4 --------------------------------------

    # doc header --------------------------------------
    header = doc.sections[0].header
    header.bottom_margin = Inches(0.2)
    head = header.paragraphs[0]
    head.text = '{Date} {Event}, {Site}\n{White} vs. {Black}   {Result}'.\
        format(Event=game_dict['Event'], \
               Site=game_dict['Site'], \
               Date=game_dict['Date'].replace('.','-'), \
               White=game_dict['White'], \
               Black=game_dict['Black'], \
               Result=game_dict['Result'])
    # doc header --------------------------------------

    # doc footer --------------------------------------
    def create_element(name):
        return(OxmlElement(name))

    def create_attribute(element, name, value):
        return(element.set(ns.qn(name), value))

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

    add_page_number(doc.sections[0].footer.paragraphs[0])
    doc.sections[0].footer.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
    #  doc footer --------------------------------------

    # first page of the booklet
    out_str = ''
    for key in game_dict.keys():
        if 'file' != key and 'pgn' != key:
            out_str = out_str + '[{k}] \"{v}\"\n'.format(k=key, v=game_dict[key])
    out_str = out_str + '\n'
    out_str = out_str + '{pgn}  {res}\n'.format(pgn=game_dict['pgn'], res=game_dict['Result'])
    doc.add_paragraph(out_str)

    # some words about the game's ECO
    if not eco_dict:
        # no eco section to print, e.g no eco found
        pass
    else:
        if not('eco' in eco_dict.keys()):
            # no eco section to print, e.g no eco found
            pass
        else:
            e = eco_dict['eco'][0]
            eco_txt = '{e} - {group}\n{eco} - {subgroup} \n{variant} \n{pgn} \n'.format( \
                                        e=e,
                                        group=eco_dict['group'],
                                        eco=eco_dict['eco'],  
                                        subgroup=eco_dict['subgroup'].replace('?',''), 
                                        variant=eco_dict['variant'].replace('?',''), 
                                        pgn=eco_dict['pgn'])
            doc.add_paragraph(eco_txt)
            
            eco_board = chess.Board(eco_dict['fen'])
            eco_tbl = doc.add_table(2, 1)
            eco_row = eco_tbl.rows[0]
            eco_row.cells[0].text = cb.board2ttf(eco_board)[:-1]
            eco_cell_paragraph = eco_row.cells[0].paragraphs[0]
            eco_cell_paragraph.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
            eco_cell_paragraph.paragraph_format.keep_with_next = True
            eco_cell_paragraph.paragraph_format.space_before = Pt(0)
            eco_cell_paragraph.paragraph_format.space_after = Pt(0)
            eco_run = eco_cell_paragraph.runs
            eco_fnt = eco_run[0].font
            eco_fnt.name = 'Chess Merida'
            eco_fnt.size = Pt(20)
            eco_row = eco_tbl.rows[1]
            eco_row.cells[0].text = eco_dict['mv']
            eco_row.cells[0].paragraphs[0].style.font.name = 'Verdana'
            eco_row.cells[0].paragraphs[0].paragraph_format.space_after = Pt(0)

    doc.add_page_break()

    #  PGN diagramms --------------------------------------
    # the PGN data for diagram genration
    boards_df = prep_ttfboards_from_pgn(game_dict['pgn'])
    
    boards_tbl = doc.add_table(2*len(boards_df), 2)
    for ix, fmv in boards_df.iterrows():

        brd_row = boards_tbl.rows[2*ix]
        
        #########################################################
        # TODO: 
        # At fmv['w_board_ttf'] tht from-/to- 
        # and check squares needs to be marked
        # therefore a paragraph needs to be split into 
        # mutiple runs, e.g.
        #   standard portion 
        #   checked - with its own text & text.font.color
        #   standard portion 
        #   from square - with its own text & bachground color
        #   standard portion 
        #   to square - with its own text & bachground color
        #   standard portion 
        # see python-docx.readthedocs.io -> Run objects class docx.text.run.Run
        #   or text.html#docx.text.paragraph.add_run
        #########################################################

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
    #  PGN diagramms --------------------------------------        
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
    ##################################################
    # for development just use 
    #   'PGN/TEST/test_do_not_change.pgn' with 5 games
    # and only its last pgn to generate one document
    # with the diagrams, at
    #   'DOCX/TEST'
    # (you have to run this 'pgn.py')
    ##################################################
    fn = get_pgnfile_names_from_dir(dir='PGN/TEST')[0]

    try:
        # check if file exists
        f = open(fn, 'r')
        f.close

        # start to get the games out of one pgn file
        games_df = get_games_from_pgnfile(fn)

        one_game_dict = games_df.iloc[1].to_dict()
        
        eco_result_dict = {}
        if 'ECO' in one_game_dict.keys():
            eco_result_dict = eco.get_eco_data_for(eco=one_game_dict['ECO'], pgn=one_game_dict['pgn'])
        else:
            eco_result_dict = eco.get_eco_data_for(eco='', pgn=one_game_dict['pgn'])

        my_doc = gen_document_from_game(one_game_dict, eco_result_dict)

        # fn fix for lichess pgn files
        event = one_game_dict['Event'].replace(
            '/', '_').replace(':', '_').replace('.', '-')
        site = one_game_dict['Site'].replace(
            '/', '_').replace(':', '_').replace('.', '-')
        
        fn = 'DOCX/TEST/' + one_game_dict['Date'].replace('.', '-') + '_' + \
                            event + '_' + \
                            site + '_( ' + \
                            one_game_dict['White'] + ' - ' + \
                            one_game_dict['Black'] + ' ).docx'
        fn = fn.replace('??','_')
        
        # store document
        ret_dict = store_document(my_doc, fn)
        print('stored:', ret_dict['file_name'])

    except IOError:
        print("File not accessible: ", fn)
    finally:
        f.close()

    return()



if __name__ == '__main__':
    main()
