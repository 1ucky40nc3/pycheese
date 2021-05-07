# -*- coding: utf-8 -*-
"""Unittests for code in the board module.

This module contains code to test the content
of the pycheese.entity module using pytest.

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


def white_pawns() -> List[Type[Pawn]]:
    """Return a list of all of white's pawns."""
    return [Pawn((i, 6), "white") for i in range(8)]


def black_pawns() -> List[Type[Pawn]]:
    """Return a list of all of black's pawns."""
    return [Pawn((i, 1), "black") for i in range(8)]


def white_pieces() -> List[Type[Piece]]:
    """Return a list of all of white's pieces. (Note: Pawns exclusive.)"""
    return [
        Rook((0, 7), "white"), 
        Knight((1, 7), "white"), 
        Bishop((2, 7), "white"), 
        Queen((3, 7), "white"), 
        King((4, 7), "white"), 
        Bishop((5, 7), "white"), 
        Knight((6, 7), "white"), 
        Rook((7, 7), "white"),
    ]


def black_pieces() -> List[Type[Piece]]:
    """Return a list of all of black's pieces. (Note: Pawns exclusive.)"""
    return [
        Rook((0, 0), "black"), 
        Knight((1, 0), "black"), 
        Bishop((2, 0), "black"), 
        Queen((3, 0), "black"), 
        King((4, 0), "black"), 
        Bishop((5, 0), "black"), 
        Knight((6, 0), "black"), 
        Rook((7, 0), "black"),
    ]


def initial_board() -> List[List[Type[Entity]]]:
    """Create a nested list of Entitys that represents the chessboard."""
    board = []

    board.append(black_pieces())
    board.append(black_pawns())

    for i in range(4):
        board.append([Empty((j, i + 2)) for j in range(8)])

    board.append(white_pawns())
    board.append(white_pieces())
    
    return board


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
    """Test the a boards `get_player_pieces` function.

    Check if the functions's behavoir is correct.
    To do so initialize an instance of the Board class
    and assert the functions output with different setups.
    """
    board = Board()

    assert_obj_func(board, "initial_board", None, initial_board())


def test_get_piece_moves():
    """Test the a boards `get_piece_moves` function.

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
    """Test the a boards `get_player_pieces` function.

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
    """Test the a boards `next_turn` function.

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


def test_case_napolean_attack() -> dict:
    """Test case for the boards `move` funtion.
    
    To test the function the follow chess game will be played:
    1. e4 e5 2. Qf3 Nc6 3. Bc4 d6 4. Qxf7#
    """
    return [
        {
            "source_coord": (4, 6),
            "target_coord": (4, 4),
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 4, 'y': 6}, 
                'target_coord': {'x': 4, 'y': 4}, 
                'event': {'type': None, 'extra': None}
            }
        },
        {
            "source_coord": (4, 1),
            "target_coord": (4, 3),
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 4, 'y': 1}, 
                'target_coord': {'x': 4, 'y': 3}, 
                'event': {'type': None, 'extra': None}
            }
        },
        {
            "source_coord": (3, 7),
            "target_coord": (5, 5),
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 3, 'y': 7}, 
                'target_coord': {'x': 5, 'y': 5}, 
                'event': {'type': None, 'extra': None}
            }
        },
        {
            "source_coord": (1, 0),
            "target_coord": (2, 2),
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 1, 'y': 0}, 
                'target_coord': {'x': 2, 'y': 2}, 
                'event': {'type': None, 'extra': None}
            }
        },
        {
            "source_coord": (5, 7),
            "target_coord": (2, 4),
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 5, 'y': 7}, 
                'target_coord': {'x': 2, 'y': 4}, 
                'event': {'type': None, 'extra': None}
            }
        },
        {
            "source_coord": (3, 1),
            "target_coord": (3, 2),
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 3, 'y': 1}, 
                'target_coord': {'x': 3, 'y': 2}, 
                'event': {'type': None, 'extra': None}
            }
        },
        {
            "source_coord": (5, 5),
            "target_coord": (5, 1),
            "promotion_target": None,
            "output": {
                'state': 'checkmate', 
                'source_coord': {'x': 5, 'y': 5}, 
                'target_coord': {'x': 5, 'y': 1}, 
                'event': {'type': 'captures', 'extra': None}
            }
        },
    ]


def test_case_castle_kingside() -> dict:
    """Test case for the boards `move` funtion.
    
    To test the function the follow chess game will be played:
    1. Nf3 Nf6 2. e3 e6 3. Be2 Be7 4. O-O O-O
    """
    return [
        {
            "source_coord": (6, 7),
            "target_coord": (5, 5),
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 6, 'y': 7}, 
                'target_coord': {'x': 5, 'y': 5}, 
                'event': {'type': None, 'extra': None}
            }
        },
        {
            "source_coord": (6, 0),
            "target_coord": (5, 2),
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 6, 'y': 0}, 
                'target_coord': {'x': 5, 'y': 2}, 
                'event': {'type': None, 'extra': None}
            }
        },
        {
            "source_coord": (4, 6),
            "target_coord": (4, 5),
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 4, 'y': 6}, 
                'target_coord': {'x': 4, 'y': 5}, 
                'event': {'type': None, 'extra': None}
            }
        },
        {
            "source_coord": (4, 1),
            "target_coord": (4, 2),
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 4, 'y': 1}, 
                'target_coord': {'x': 4, 'y': 2}, 
                'event': {'type': None, 'extra': None}
            }
        },
        {
            "source_coord": (5, 7),
            "target_coord": (4, 6),
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 5, 'y': 7}, 
                'target_coord': {'x': 4, 'y': 6}, 
                'event': {'type': None, 'extra': None}
            }
        },
        {
            "source_coord": (5, 0),
            "target_coord": (4, 1),
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 5, 'y': 0}, 
                'target_coord': {'x': 4, 'y': 1}, 
                'event': {'type': None, 'extra': None}
            }
        },
        {
            "source_coord": (4, 7),
            "target_coord": (6, 7),
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 4, 'y': 7}, 
                'target_coord': {'x': 6, 'y': 7}, 
                'event': {'type': 'castle', 'extra': 'kingside'}
            }
        },
        {
            "source_coord": (4, 0),
            "target_coord": (6, 0),
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 4, 'y': 0}, 
                'target_coord': {'x': 6, 'y': 0}, 
                'event': {'type': 'castle', 'extra': 'kingside'}
            }
        },
    ]


def test_case_castle_queenside() -> dict:
    """Test case for the boards `move` funtion.
    
    To test the function the follow chess game will be played:
    1. Nc3 Nc6 2. d3 d6 3. Be3 Be6 4. Qd2 Qd7 5. O-O-O O-O-O
    """
    return [
        {
            "source_coord": (1, 7),
            "target_coord": (2, 5),
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 1, 'y': 7}, 
                'target_coord': {'x': 2, 'y': 5}, 
                'event': {'type': None, 'extra': None}
            }
        },
        {
            "source_coord": (1, 0),
            "target_coord": (2, 2),
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 1, 'y': 0}, 
                'target_coord': {'x': 2, 'y': 2}, 
                'event': {'type': None, 'extra': None}
            }
        },
        {
            "source_coord": (3, 6),
            "target_coord": (3, 5),
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 3, 'y': 6}, 
                'target_coord': {'x': 3, 'y': 5}, 
                'event': {'type': None, 'extra': None}
            }
        },
        {
            "source_coord": (3, 1),
            "target_coord": (3, 2),
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 3, 'y': 1}, 
                'target_coord': {'x': 3, 'y': 2}, 
                'event': {'type': None, 'extra': None}
            }
        },
        {
            "source_coord": (2, 7),
            "target_coord": (4, 5),
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 2, 'y': 7}, 
                'target_coord': {'x': 4, 'y': 5}, 
                'event': {'type': None, 'extra': None}
            }
        },
        {
            "source_coord": (2, 0),
            "target_coord": (4, 2),
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 2, 'y': 0}, 
                'target_coord': {'x': 4, 'y': 2}, 
                'event': {'type': None, 'extra': None}
            }
        },
        {
            "source_coord": (3, 7),
            "target_coord": (3, 6),
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 3, 'y': 7}, 
                'target_coord': {'x': 3, 'y': 6}, 
                'event': {'type': None, 'extra': None}
            }
        },
        {
            "source_coord": (3, 0),
            "target_coord": (3, 1),
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 3, 'y': 0}, 
                'target_coord': {'x': 3, 'y': 1}, 
                'event': {'type': None, 'extra': None}
            }
        },
        {
            "source_coord": (4, 7),
            "target_coord": (2, 7),
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 4, 'y': 7}, 
                'target_coord': {'x': 2, 'y': 7}, 
                'event': {'type': 'castle', 'extra': 'queenside'}
            }
        },
        {
            "source_coord": (4, 0),
            "target_coord": (2, 0),
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 4, 'y': 0}, 
                'target_coord': {'x': 2, 'y': 0}, 
                'event': {'type': 'castle', 'extra': 'queenside'}
            }
        },
    ]


def test_move():
    """Test the boards `move` funtion.

    Check if the functions's behavoir is correct.
    To do so initialize an instance of the Board class
    and assert the functions output with different setups.
    """
    test_cases = [
        test_case_napolean_attack(),
        test_case_castle_kingside(),
        test_case_castle_queenside(),
    ]

    for case in test_cases:
        board = Board()

        for move in case:
            source_coord = move["source_coord"]
            target_coord = move["target_coord"]

            promotion_target = move["promotion_target"]
            
            output = board.move(
                source_coord, target_coord, promotion_target)

            print(board.show())

            assert output == move["output"]