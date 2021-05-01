# -*- coding: utf-8 -*-
"""Unittests for code in the entity module.

This module contains code to test the content
of the pycheese.entity module using pytest.

Example:
    To run the tests you can for example:
        - Run the pytest command from the command line:
            ..> pytest
        - Run the tests.py file in the repos top-level:
            ..> python tests.py
"""


from typing import Type
from typing import Tuple

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


def test_entity():
    """Test the functionality of the abstract Entity class.

    Check if the Entity class`s behavoir is accordingly.
    To do so initialize an instance of the abstract class and
    instances of the first-level children of the abstract class.
    Assert their behavior.
    """
    # Sample values
    coord = (0, 0)
    player = "white"
    moves = ((0, 0),)

    # Instance of the abstract class
    entity = Entity(coord)
    # Instances of first level children of the abstract class.
    empty = Empty(coord)
    piece = Piece(coord, player, moves)

    for obj in [entity, empty, piece]:
        assert_obj_attr(obj, "_Entity__coord", coord)
        assert_obj_attr(obj, "_Entity__attacked", False)

        assert_obj_func(obj, "set_coord", [(1, 1)], None)
        assert_obj_func(obj, "get_coord", None, (1, 1))

        assert_obj_func(obj, "set_attacked", [True], None)
        assert_obj_func(obj, "is_attacked", None, True)


def test_piece():
    """Test the functionality of the abstract Piece class.

    Check if the Piece class`s behavoir is accoordingly.
    To do so initialize an instance of the abstract class and
    instances of the first-level children of the abstract class.
    Assert their behavior.
    """
    # Sample values
    coord = (0, 0)
    player = "white"
    moves = ((0, 0),)

    # Instance of the abstract class
    piece = Piece(coord, player, moves)
    # Instances of first level children of the abstract class.
    pawn = Pawn(coord, player)
    knight = Knight(coord, player)
    bishop = Bishop(coord, player)
    rook = Rook(coord, player)
    queen = Queen(coord, player)
    king = King(coord, player)

    def _moves(obj: Type[Piece]) -> Tuple[Tuple[int, int]]: 
        """Get a class`s moves if moves is a class attribute."""
        return type(obj).moves if "moves" in dir(type(obj)) else moves

    for obj in [piece, pawn, knight, bishop, rook, queen, king]:
        assert_obj_attr(obj, "_Entity__coord", coord)

        assert_obj_attr(obj, "_Piece__player", player)
        assert_obj_attr(obj, "_Piece__moves", _moves(obj))

        
        assert_obj_attr(obj, "_Piece__attacker", None)
        assert_obj_attr(obj, "_Piece__pinned", False)

        assert_obj_func(obj, "set_coord", [(1, 1)], None)
        assert_obj_func(obj, "get_coord", None, (1, 1))

        assert_obj_func(obj, "get_player", None, player)
        assert_obj_func(obj, "get_moves", None, _moves(obj))

        assert_obj_func(obj, "set_attacked", [True], None)
        assert_obj_func(obj, "is_attacked", None, True)

        assert_obj_func(obj, "set_pinned", [True], None)
        assert_obj_func(obj, "is_pinned", None, (True))
        assert_obj_func(obj, "set_attacker", [piece], None)
        assert_obj_func(obj, "get_attacker", None, piece)

        assert "__hash__" in dir(obj)

    pawn_json = {'type': 'Pawn', 'player': 'white', 'coord': {'x': 1, 'y': 1}, 'pinned': True, 'attacker': (1, 1)}
    assert pawn_json == pawn.to_json()

    
