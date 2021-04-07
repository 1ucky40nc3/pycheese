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


from typing import Union
from typing import List
from typing import Any
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


def assert_obj_attr(obj: object, attr: str, target: object):
    """Assert a objects attribute.

    First the code will assert if the given object has the
    attribute that is to be checked. Secondly it the code
    will assert of the attributes value is the target.

    Args:
        obj (:obj:): The object whose attribute is to be checked.
        attr (str): The name of the attribute which is to be checked.
        target (:obj:): The target value of the attribute in question.
    """
    assert attr in dir(obj)
    assert getattr(obj, attr) == target


def assert_obj_func(obj: object, func: str, param: Union[List[Any], None], target: object):
    """Assert a objects function.

    First the code will assert if the given object has the
    function that is to be checked. Secondly it the code
    will assert of the functions return value is the target.

    Args:
        obj (:obj:): The object whose attribute is to be checked.
        func (str): The name of the function which is to be checked.
        param (:obj:, optional): Parameters for the function call.
        target (:obj:): The target value of the attribute in question.
    """
    assert func in dir(type(obj))

    if param:
        assert getattr(obj, func)(*param) == target
    else:
        assert getattr(obj, func)() == target


def test_entity():
    """Test the functionality of the abstract Entity class.

    Check if the Entity class`s behavoir is accordingly.
    To do so initialize an instance of the abstract class and
    instances of the first-level children of the abstract class.
    Assert their behavior.
    """
    # Sample values
    cord = (0, 0)
    player = "white"
    moves = ((0, 0),)

    # Instance of the abstract class
    entity = Entity(cord)
    # Instances of first level children of the abstract class.
    empty = Empty(cord)
    piece = Piece(cord, player, moves)

    for obj in [entity, empty, piece]:
        assert_obj_attr(obj, "_Entity__cord", cord)

        assert_obj_func(obj, "set_cord", [(1, 1)], None)
        assert_obj_func(obj, "get_cord", None, (1, 1))


def test_piece():
    """Test the functionality of the abstract Piece class.

    Check if the Piece class`s behavoir is accordingly.
    To do so initialize an instance of the abstract class and
    instances of the first-level children of the abstract class.
    Assert their behavior.
    """
    # Sample values
    cord = (0, 0)
    player = "white"
    moves = ((0, 0),)

    # Instance of the abstract class
    piece = Piece(cord, player, moves)
    # Instances of first level children of the abstract class.
    pawn = Pawn(cord, player)
    knight = Knight(cord, player)
    bishop = Bishop(cord, player)
    rook = Rook(cord, player)
    queen = Queen(cord, player)
    king = King(cord, player)

    def _moves(obj: Type[Piece]) -> Tuple[Tuple[int, int]]: 
        """Get a class`s moves if moves is a class attribute."""
        return type(obj).moves if "moves" in dir(type(obj)) else moves

    for obj in [piece, pawn, knight, bishop, rook, queen, king]:
        assert_obj_attr(obj, "_Entity__cord", cord)

        assert_obj_attr(obj, "_Piece__player", player)
        assert_obj_attr(obj, "_Piece__moves", _moves(obj))

        assert_obj_attr(obj, "_Piece__attacked", False)
        assert_obj_attr(obj, "_Piece__attacker", None)
        assert_obj_attr(obj, "_Piece__pinned", False)

        assert_obj_func(obj, "set_cord", [(1, 1)], None)
        assert_obj_func(obj, "get_cord", None, (1, 1))

        assert_obj_func(obj, "get_player", None, player)
        assert_obj_func(obj, "get_moves", None, _moves(obj))

        assert_obj_func(obj, "set_attacked", [True], None)
        assert_obj_func(obj, "is_attacked", None, True)
        assert_obj_func(obj, "set_pinned", [True], None)
        assert_obj_func(obj, "is_pinned", None, (True))
        assert_obj_func(obj, "set_attacker", [piece], None)
        assert_obj_func(obj, "get_attacker", None, piece)

