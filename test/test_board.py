# -*- coding: utf-8 -*-
"""Unittests for code in the board module.

This module contains code to test the content
of the pycheese.core.board module using pytest.

Example:
    To run the tests you can for example:
        - Run the pytest command from the command line:
            ..> pytest
        - Run the tests.py file in the repos top-level:
            ..> python tests.py
"""

from pycheese.core.utils import dict_to_coord
from typing import List
from typing import Type

from pycheese.core.board import Board

from test.utils import assert_obj_attr
from test.utils import assert_obj_func
from test.utils import white_pawns
from test.utils import black_pawns
from test.utils import white_pieces
from test.utils import black_pieces
from test.utils import initial_board

from pycheese.core.entity import Pawn
from pycheese.core.entity import Knight
from pycheese.core.entity import Bishop
from pycheese.core.entity import Rook
from pycheese.core.entity import Queen
from pycheese.core.entity import King

from test.cases.cases_board_to_dict import case_initial_board
from test.cases.cases_board_to_dict import case_rook_checkmate_board
from test.cases.cases_board_to_dict import case_napoleon_attack_board
from test.cases.cases_board_to_dict import case_queen_check_empty_board
from test.cases.cases_board_to_dict import case_and_king_queen_stalemate_board
from test.cases.cases_board_to_dict import case_promotion_empty_board
from test.cases.cases_board_to_dict import case_promotion_checkmate_empty_board
from test.cases.cases_board_to_dict import case_check_by_castle_board
from test.cases.cases_board_to_dict import case_promotion_empty_bishop_draw_board
from test.cases.cases_board_to_dict import case_promotion_empty_bishop_no_draw_board


from test.cases.cases_board_move import case_napoleon_attack
from test.cases.cases_board_move import case_rook_checkmate
from test.cases.cases_board_move import case_queen_check_empty
from test.cases.cases_board_move import case_castle_kingside
from test.cases.cases_board_move import case_castle_queenside
from test.cases.cases_board_move import case_and_king_queen_stalemate
from test.cases.cases_board_move import case_promotion_empty
from test.cases.cases_board_move import case_promotion_checkmate_empty
from test.cases.cases_board_move import case_check_by_castle
from test.cases.cases_board_move import case_promotion_empty_bishop_draw
from test.cases.cases_board_move import case_promotion_empty_bishop_no_draw


def test_board():
    """Test the functionality of the Board class.

    Check if the Boards class`s behavoir is correct.
    To do so initialize an instance of the class and assert
    attribute and function functionality.
    """
    board = Board()

    assert_obj_attr(board, "state", "ongoing")
    assert_obj_attr(board, "player", "white")
    assert_obj_attr(board, "board", initial_board())


def test_get_piece_options():
    """Test a boards `get_piece_options` function.

    Check if the functions's behavoir is correct.
    To do so initialize an instance of the Board class
    and assert the functions output with different setups.
    """
    board = Board()

    cases = [
        {
            "name": "white Pawn at a2 - with empty options",
            "board": {
                'state': 'ongoing', 
                'player': 'white',
                'last': {},
                'pieces': [
                    {'type': 'Pawn', 'player': 'white', 'coord': {'x': 0, 'y': 6}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
                    {'type': 'King', 'player': 'white', 'coord': {'x': 4, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
                    {'type': 'King', 'player': 'black', 'coord': {'x': 4, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}
                ]
            },
            "piece_coord": {"x": 0, "y": 6},
            "piece_options": ([[0, 5], [0, 4]], [])
        },
        {
            "name": "white Pawn at a2 - with options",
            "board": {
                'state': 'ongoing', 
                'player': 'white',
                'last': {},
                'pieces': [
                    {'type': 'Pawn', 'player': 'white', 'coord': {'x': 0, 'y': 6}, 'options': {'moves': [[0, 5], [0, 4]], 'others': []}, 'pinned': False, 'pinner': None}, 
                    {'type': 'King', 'player': 'white', 'coord': {'x': 4, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
                    {'type': 'King', 'player': 'black', 'coord': {'x': 4, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}
                ]
            },
            "piece_coord": {"x": 0, "y": 6},
            "piece_options": ([[0, 5], [0, 4]], [])
        },
        {
            "name": "white Pawn at a2 - blocked by king",
            "board": {
                'state': 'ongoing', 
                'player': 'white',
                'last': {},
                'pieces': [
                    {'type': 'Pawn', 'player': 'white', 'coord': {'x': 0, 'y': 6}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
                    {'type': 'King', 'player': 'white', 'coord': {'x': 0, 'y': 5}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
                    {'type': 'King', 'player': 'black', 'coord': {'x': 4, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}
                ]
            },
            "piece_coord": {'x': 0, 'y': 6},
            "piece_options": ([], [])
        },
        {
            "name": "pinned white knight - empty board",
            "board": {
                'state': 'ongoing', 
                'player': 'white',
                'last': {}, 
                'pieces': [
                    {'type': 'Knight', 'player': 'white', 'coord': {'x': 4, 'y': 6}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
                    {'type': 'King', 'player': 'white', 'coord': {'x': 4, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
                    {'type': 'Queen', 'player': 'black', 'coord': {'x': 4, 'y': 1}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
                    {'type': 'King', 'player': 'black', 'coord': {'x': 4, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}
                ]
            },
            "piece_coord": {'x': 4, 'y': 6},
            "piece_options": ([], [])
        },
        {
            "name": "pinned white rook - empty board",
            "board": {
                'state': 'ongoing', 
                'player': 'white',
                'last': {},
                'pieces': [
                    {'type': 'Rook', 'player': 'white', 'coord': {'x': 4, 'y': 6}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
                    {'type': 'King', 'player': 'white', 'coord': {'x': 4, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
                    {'type': 'Queen', 'player': 'black', 'coord': {'x': 4, 'y': 1}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
                    {'type': 'King', 'player': 'black', 'coord': {'x': 4, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}
                ]
            },
            "piece_coord": {'x': 4, 'y': 6},
            "piece_options": ([[4, 5], [4, 4], [4, 3], [4, 2], [4, 1]], [])
        },
        {
            "name": "king moves - before rook checkmate",
            "board": case_rook_checkmate_board(),
            "piece_coord": {'x': 7, 'y': 0},
            "piece_options": ([[6, 0]], [])
        },
        {
            "name": "king moves - castle blocked by other player",
            "board": {
                'state': 'ongoing', 
                'player': 'white',
                'last': {},
                'pieces': [
                    {'type': 'Rook', 'player': 'white', 'coord': {'x': 7, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
                    {'type': 'King', 'player': 'white', 'coord': {'x': 4, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
                    {'type': 'Rook', 'player': 'black', 'coord': {'x': 5, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
                    {'type': 'King', 'player': 'black', 'coord': {'x': 4, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}
                ]
            },
            "piece_coord": {'x': 4, 'y': 7},
            "piece_options": ([[4, 6], [3, 7], [3, 6]], [])
        },
        {
            "name": "king moves - cant castle because enemy check",
            "board": {
                'state': 'ongoing', 
                'player': 'white',
                'last': {'x': 4, 'y': 1},
                'pieces': [
                    {'type': 'Rook', 'player': 'white', 'coord': {'x': 7, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
                    {'type': 'King', 'player': 'white', 'coord': {'x': 4, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
                    {'type': 'Rook', 'player': 'black', 'coord': {'x': 4, 'y': 1}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
                    {'type': 'King', 'player': 'black', 'coord': {'x': 4, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}
                ]
            },
            "piece_coord": {'x': 4, 'y': 7},
            "piece_options": ([[5, 7], [3, 7], [3, 6], [5, 6]], [])
        },
        {
            "name": "rook moves - resolve check by capturing",
            "board": {
                'state': 'check', 
                'player': 'white',
                'last': {'x': 6, 'y': 6},
                'pieces': [
                    {'type': 'Rook', 'player': 'white', 'coord': {'x': 4, 'y': 6}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
                    {'type': 'King', 'player': 'white', 'coord': {'x': 4, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
                    {'type': 'Knight', 'player': 'black', 'coord': {'x': 6, 'y': 6}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
                    {'type': 'King', 'player': 'black', 'coord': {'x': 4, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}
                ]
            },
            "piece_coord": {'x': 4, 'y': 6},
            "piece_options": ([[6, 6]], [])
        }
    ]

    for case in cases:
        print(case["name"])
        board.from_dict(case["board"])

        x, y = dict_to_coord(case["piece_coord"])
        piece = board.get()[y][x]

        print(board.get_piece_options(piece))
        assert sorted(board.get_piece_options(piece)) == sorted(case["piece_options"])


def test_get_player_pieces():
    """Test a boards `get_player_pieces` function.

    Check if the functions's behavoir is correct.
    To do so initialize an instance of the Board class
    and assert the functions output with different setups.
    """
    board = Board()

    cases = [
        {
            "name": "only kings on board",
            "board": {
                'state': 'ongoing', 
                'player': 'white',
                'last': {},
                'pieces': [
                    {'type': 'King', 'player': 'white', 'coord': {'x': 4, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
                    {'type': 'King', 'player': 'black', 'coord': {'x': 4, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}
                ]
            },
            "white_pieces": [King([4, 7], "white")],
            "black_pieces": [King([4, 0], "black")]
        },
        {
            "name": "only kings a one pawn per player",
            "board": {
                'state': 'ongoing', 
                'player': 'white',
                'last': {},
                'pieces': [
                    {'type': 'Pawn', 'player': 'white', 'coord': {'x': 0, 'y': 6}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
                    {'type': 'King', 'player': 'white', 'coord': {'x': 4, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
                    {'type': 'Pawn', 'player': 'black', 'coord': {'x': 0, 'y': 1}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
                    {'type': 'King', 'player': 'black', 'coord': {'x': 4, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}
                ]
            },
            "white_pieces": [Pawn([0, 6], "white"), King([4, 7], "white")],
            "black_pieces": [Pawn([0, 1], "black"), King([4, 0], "black")]
        },
        {
            "name": "initial board",
            "board": Board().to_dict(),
            "white_pieces": white_pawns() + white_pieces(),
            "black_pieces": black_pawns() + black_pieces()
        }
    ]

    for case in cases:
        print(case["name"])
        board.from_dict(case["board"])

        assert set(board.get_player_pieces("white")) == set(case["white_pieces"])
        assert set(board.get_player_pieces("black")) == set(case["black_pieces"])


def test_next_turn():
    """Test a boards `next_turn` function.

    Check if the functions's behavoir is correct.
    To do so initialize an instance of the Board class
    and assert the functions output with different setups.
    """
    board = Board()

    assert_obj_attr(board, "player", "white")
    assert_obj_func(board, "next_turn", None, None)

    assert_obj_attr(board, "player", "black")
    assert_obj_func(board, "next_turn", None, None)
    
    assert_obj_attr(board, "player", "white")


def test_to_dict():
    """Test a boards `to_json` function.

    Check if the functions's behavoir is correct.
    To do so initialize an instance of the Board class
    and assert the functions output with different setups.
    """
    cases = [
        case_initial_board(),
    ]

    for case in cases:
        board = Board()

        assert board.to_dict() == case


def test_from_dict():
    """Test a boards `from_dict` function.

    Check if the functions's behavoir is correct.
    To do so initialize an instance of the Board class
    and assert the functions output with different setups.
    """
    cases = [
        {
            "name": "initial board - from board", 
            "board": Board().to_dict()
        },
        {
            "name": "initial board - from case", 
            "board": case_initial_board()
        },
    ]
    
    for case in cases:
        print(case["name"])

        board = Board(case["board"])
        assert board.to_dict() == case["board"]

        board.from_dict(case["board"])
        assert board.to_dict() == case["board"]


def test_move():
    """Test the boards `move` function.

    Check if the functions's behavoir is correct.
    To do so initialize an instance of the Board class
    and assert the functions output with different setups.
    """
    cases = [
        {
            "name": "napoleon attack",
            "board": Board().to_dict(),
            "moves": case_napoleon_attack()
        },
        {
            "name": "queen check empty board",
            "board": case_queen_check_empty_board(),
            "moves": case_queen_check_empty()
        },
        {
            "name": "rook checkmate",
            "board": case_rook_checkmate_board(),
            "moves": case_rook_checkmate()
        },
        {
            "name": "castle kingside",
            "board": Board().to_dict(),
            "moves": case_castle_kingside(),
        },
        {
            "name": "castle queenside",
            "board": Board().to_dict(),
            "moves": case_castle_queenside(),
        },
        {
            "name": "check by castling",
            "board": case_check_by_castle_board(),
            "moves": case_check_by_castle()
        },
        {
            "name": "king & queen stalemate",
            "board": case_and_king_queen_stalemate_board(),
            "moves": case_and_king_queen_stalemate()
        },
        {
            "name": "promotion - empty board",
            "board": case_promotion_empty_board(),
            "moves": case_promotion_empty()
        },
        {
            "name": "promotion checkmate - empty board",
            "board": case_promotion_checkmate_empty_board(),
            "moves": case_promotion_checkmate_empty()
        },
        {
            "name": "promotion to bishop - draw - empty board",
            "board": case_promotion_empty_bishop_draw_board(),
            "moves": case_promotion_empty_bishop_draw()
        },
        {
            "name": "promotion to bishop - draw - empty board",
            "board": case_promotion_empty_bishop_no_draw_board(),
            "moves": case_promotion_empty_bishop_no_draw()
        }
    ]

    for case in cases:
        print(case["name"])
        board = Board(case["board"])

        for move in case["moves"]:
            source_coord = move["source_coord"]
            target_coord = move["target_coord"]

            promotion_target = move["promotion_target"]

            output = board.move(
                source_coord, target_coord, promotion_target)

            assert output == move["output"]