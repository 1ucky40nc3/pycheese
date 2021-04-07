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


def initial_board() -> List[List[Type[Entity]]]:
    """Create a nested list of Entitys that represents the chessboard."""
    board = []

    board.append([
        Rook((0, 0), "black"), 
        Knight((1, 0), "black"), 
        Bishop((2, 0), "black"), 
        Queen((3, 0), "black"), 
        King((4, 0), "black"), 
        Bishop((5, 0), "black"), 
        Knight((6, 0), "black"), 
        Rook((7, 0), "black"),
    ])
    board.append([Pawn((i, 1), "black") for i in range(8)])

    for i in range(4):
        board.append([Empty((j, i + 2)) for j in range(8)])

    board.append([Pawn((i, 6), "white") for i in range(8)])
    board.append([
        Rook((0, 7), "white"), 
        Knight((1, 7), "white"), 
        Bishop((2, 7), "white"), 
        Queen((3, 7), "white"), 
        King((4, 7), "white"), 
        Bishop((5, 7), "white"), 
        Knight((6, 7), "white"), 
        Rook((7, 7), "white"),
    ])
    
    return board

def test_board():
    """Test the functionality of the Board class.

    Check if the Entity class`s behavoir is accordingly.
    To do so initialize an instance of the class and assert
    attribute and function functionality.
    """
    board = Board()

    assert_obj_attr(board, "state", "ongoing")
    assert_obj_attr(board, "player", "white")
    assert_obj_attr(board, "board", initial_board())

    assert_obj_func(board, "initial_board", None, initial_board())
    # assert_obj_func(board, "__call__", )

