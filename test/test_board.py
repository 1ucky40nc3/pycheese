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

from typing import List
from typing import Type

from pycheese.core.board import Board

from pycheese.core.entity import Entity
from pycheese.core.entity import Empty
from pycheese.core.entity import Piece
from pycheese.core.entity import Pawn
from pycheese.core.entity import Knight
from pycheese.core.entity import Bishop
from pycheese.core.entity import Rook
from pycheese.core.entity import Queen
from pycheese.core.entity import King

from test.utils import assert_obj_attr
from test.utils import assert_obj_func
from test.utils import white_pawns
from test.utils import black_pawns
from test.utils import white_pieces
from test.utils import black_pieces
from test.utils import initial_board

from test.cases.cases_board_to_json import case_initial_board
from test.cases.cases_board_to_json import case_napolean_attack_board

from test.cases.cases_board_move import case_napolean_attack
from test.cases.cases_board_move import case_castle_kingside
from test.cases.cases_board_move import case_castle_queenside


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


def test_initial_board():
    """Test a boards `get_player_pieces` function.

    Check if the functions's behavoir is correct.
    To do so initialize an instance of the Board class
    and assert the functions output with different setups.
    """
    board = Board()

    assert_obj_func(board, "initial_board", None, initial_board())


def test_get_piece_moves():
    """Test a boards `get_piece_moves` function.

    Check if the functions's behavoir is correct.
    To do so initialize an instance of the Board class
    and assert the functions output with different setups.
    """
    board = Board()

    test_cases = [
        {
            "piece_moves": ([], []),
            "coord": {"x": 0, "y": 7}
        },
        {
            "piece_moves": ([(0, 5), (0, 4)], []),
            "coord": {"x": 0, "y": 6}
        }
    ]

    for case in test_cases:
        x, y = case["coord"]["x"], case["coord"]["y"]

        piece = board.board[y][x]
        board_piece_moves = board.get_piece_moves(piece, (x, y))

        assert sorted(board_piece_moves) == sorted(case["piece_moves"])


def test_get_player_pieces():
    """Test a boards `get_player_pieces` function.

    Check if the functions's behavoir is correct.
    To do so initialize an instance of the Board class
    and assert the functions output with different setups.
    """
    board = Board()

    # Test the function with the initial board for `white`. And no `board` parameter.
    player_pieces = white_pawns() + white_pieces()
    board_player_pieces = board.get_player_pieces("white")

    assert set(player_pieces) == set(board_player_pieces)

    # Test the function with the initial board for `black`. And no `board` parameter.
    player_pieces = black_pawns() + black_pieces()
    board_player_pieces = board.get_player_pieces("black")

    assert set(player_pieces) == set(board_player_pieces)

    # Test the function with the initial board for `black`. With `board` parameter.
    board_player_pieces = board.get_player_pieces("black", board=board.board)

    assert set(player_pieces) == set(board_player_pieces)


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


def test_to_json():
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

        assert board.to_json() == case


def test_from_json():
    """Test a boards `from_json` function.

    Check if the functions's behavoir is correct.
    To do so initialize an instance of the Board class
    and assert the functions output with different setups.
    """
    cases = [
        case_initial_board(),
        case_napolean_attack_board(),
    ]
    
    for case in cases:
        board = Board(case)
        assert board.to_json() == case

        board.from_json(case)
        assert board.to_json() == case


def test_move():
    """Test the boards `move` funtion.

    Check if the functions's behavoir is correct.
    To do so initialize an instance of the Board class
    and assert the functions output with different setups.
    """
    cases = [
        case_napolean_attack(),
        case_castle_kingside(),
        case_castle_queenside(),
    ]

    for case in cases:
        board = Board()

        for move in case:
            source_coord = move["source_coord"]
            target_coord = move["target_coord"]

            promotion_target = move["promotion_target"]
            
            output = board.move(
                source_coord, target_coord, promotion_target)

            assert output == move["output"]