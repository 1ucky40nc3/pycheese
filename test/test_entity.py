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

Todos:
    * TODO: update test for classes with 'pseudo immutable' attributes
"""


from typing import Union
from typing import List
from typing import Any
from typing import Type

from pycheese.entity import Entity
from pycheese.entity import Empty
from pycheese.entity import Piece
from pycheese.entity import Pawn
from pycheese.entity import Knight
from pycheese.entity import Bishop
from pycheese.entity import Rook
from pycheese.entity import Queen
from pycheese.entity import King


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
    member = "white"
    moves = ((0, 0),)

    # Instance of the abstract class
    entity = Entity(cord)
    # Instances of first level children of the abstract class.
    empty = Empty(cord)
    piece = Piece(cord, member, moves)

    for obj in [entity, empty, piece]:
        assert_obj_attr(obj, "cord", cord)
        assert_obj_attr(obj, "attacked", False)
        assert_obj_attr(obj, "attacker", None)
        assert_obj_attr(obj, "pinned", False)

        assert_obj_func(obj, "set_attacked", [True], None)
        assert_obj_func(obj, "is_attacked", None, True)
        assert_obj_func(obj, "set_pinned", [True, piece], None)
        assert_obj_func(obj, "is_pinned", None, (True, piece))


def test_piece():
    """Test the functionality of the abstract Piece class.

    Check if the Piece class`s behavoir is accordingly.
    To do so initialize an instance of the abstract class and
    instances of the first-level children of the abstract class.
    Assert their behavior.
    """
    # Sample values
    cord = (0, 0)
    member = "white"
    moves = ((0, 0),)

    # Instance of the abstract class
    piece = Piece(cord, member, moves)
    # Instances of first level children of the abstract class.
    pawn = Pawn(cord, member)
    knight = Knight(cord, member)
    bishop = Bishop(cord, member)
    rook = Rook(cord, member)
    queen = Queen(cord, member)
    king = King(cord, member)

    def _moves(obj: Type[Piece]): 
        """Get a class`s moves if moves is a class attribute."""
        return type(obj).moves if "moves" in dir(type(obj)) else moves

    for obj in [piece, pawn, knight, bishop, rook, queen, king]:
        assert_obj_attr(obj, "cord", cord)
        assert_obj_attr(obj, "attacked", False)
        assert_obj_attr(obj, "attacker", None)
        assert_obj_attr(obj, "pinned", False)

        assert_obj_attr(obj, "member", member)
        assert_obj_attr(obj, "moves", _moves(obj))

        assert_obj_func(obj, "set_attacked", [True], None)
        assert_obj_func(obj, "is_attacked", None, True)
        assert_obj_func(obj, "set_pinned", [True, piece], None)
        assert_obj_func(obj, "is_pinned", None, (True, piece))

        assert_obj_func(obj, "get_moves", None, _moves(obj))
        assert_obj_func(obj, "membership", None, member)
        assert_obj_func(obj, "set_cord", [(1, 1)], None)
        assert_obj_func(obj, "get_cord", None, (1, 1))