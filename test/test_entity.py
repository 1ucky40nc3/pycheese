# -*- coding: utf-8 -*-
"""Unittests for code in the entity module.

This module contains code to test the content
of the pycheese.core.entity module using pytest.

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

from pycheese.core.utils import coord_to_dict

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

        
        assert_obj_attr(obj, "_Piece__pinner", None)
        assert_obj_attr(obj, "_Piece__pinned", False)

        assert_obj_func(obj, "set_coord", [(1, 1)], None)
        assert_obj_func(obj, "get_coord", None, (1, 1))

        assert_obj_func(obj, "get_player", None, player)
        assert_obj_func(obj, "get_moves", None, _moves(obj))

        assert_obj_func(obj, "get_options", None, {"moves":[], "others": []})
        assert_obj_func(obj, "set_options", [{"moves":[(1, 1)], "others": []}], None)
        assert_obj_func(obj, "get_options", None, {"moves":[(1, 1)], "others": []})

        assert_obj_func(obj, "set_attacked", [True], None)
        assert_obj_func(obj, "is_attacked", None, True)

        assert_obj_func(obj, "set_pinned", [True], None)
        assert_obj_func(obj, "is_pinned", None, (True))
        assert_obj_func(obj, "set_pinner", [(1, 1)], None)
        assert_obj_func(obj, "get_pinner", None, (1, 1))

        # Test object has functions. Note: Theese funcs are hard to test at large scale.
        # Therefore theese functions will be tested selectively in the following code.
        assert "to_dict" in dir(obj)
        assert "__hash__" in dir(obj)



    # Test a `Pawn`'s special functionality.
    # Test with existing instance.
    assert_obj_attr(pawn, "_Pawn__start_coord", coord)
    assert_obj_func(pawn, "can_special", None, False)

    # Test with new instance.
    pawn = Pawn(coord, player)
    assert_obj_func(pawn, "can_special", None, True)
    
    # Test a `Rook`'s and a `King`'s special functionality.
    assert_obj_attr(rook, "_Rook__moved", False)
    assert_obj_attr(king, "_King__moved", False)

    assert_obj_func(rook, "did_move", None, None)
    assert_obj_func(king, "did_move", None, None)

    assert_obj_func(rook, "get_moved", None, True)
    assert_obj_func(king, "get_moved", None, True)



    
def test_to_dict():
    """Test the `to_dict` function of a abstract Piece instance.

    Check if the Piece class`s behavoir is accoordingly.
    To do so initialize an instance of the abstract class and
    instances of the first-level children of the abstract class.
    Assert their behavior.
    """
    pieces = {"Pawn": Pawn, "Knight": Knight, "Bishop": Bishop, "Rook": Rook, "Queen": Queen, "King": King}

    player = "white"
    coord = [0, 0]
    coord_ = [1, 1]
    options = {"moves": [], "others": []}
    options_ = {"moves": [coord_], "others": []}
    

    for name, cls in pieces.items():
        piece = cls(coord, "white")
        dict = {'type': name, 'player': 'white', 'coord': coord_to_dict(coord), 'options': options, 'pinned': False, 'pinner': None}
        
        assert piece.to_dict() == dict

        piece.set_coord(coord_)
        piece.set_options(options_)
        piece.set_pinned(True)
        piece.set_pinner(coord_)

        dict = {'type': name, 'player': 'white', 'coord': coord_to_dict(coord_), 'options': options_, 'pinned': True, 'pinner': coord_to_dict(coord_)}

        assert piece.to_dict() == dict