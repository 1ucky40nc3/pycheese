# -*- coding: utf-8 -*-
"""Utils for package modules.

This module contains code that ensures the functionality
of the package in the sustainable way.
"""


from typing import Union
from typing import List
from typing import Any


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