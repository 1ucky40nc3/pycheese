# -*- coding: utf-8 -*-
"""Utils for package modules.

This module contains code that ensures the functionality
of the package in the sustainable way.
"""


from typing import Type
from typing import List
from typing import Tuple
from typing import Union

from pycheese.core.entity import Entity
from pycheese.core.entity import Empty
from pycheese.core.entity import Piece
from pycheese.core.entity import Pawn
from pycheese.core.entity import Knight
from pycheese.core.entity import Bishop
from pycheese.core.entity import Rook
from pycheese.core.entity import Queen
from pycheese.core.entity import King

from pycheese.core.error import NotWhitelistedException


def initial_board(self) -> List[List[Type[Entity]]]:
    """Create a nested list of Entitys that represents the chess board.

    Note:
        The chess board is build with the position 
        'a8' at the coordinate (0, 0) (h1 --> (7, 7)).
        Reminder: Coordinates have to be translated!
        This function is called in the constructor.

    Example:
        >>> from pycheese.core.board import Board
        >>> from pycheese.core.utils import initial_board
        >>> board = Board()
        >>> board.set(initial_board())
        >>> print(board.show())
        ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
        ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ 
        ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
        ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
        ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
        ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
        ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙
        ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖

    Returns:
        list: Nested list of Entitys that represents the chess board.
    """
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

def empty_board(self) -> List[List[Type[Entity]]]:
    """Create a nested list of Entitys that represents an empty chess board.

    Note:
        The chess board is build with the position 
        'a8' at the coordinate (0, 0) (h1 --> (7, 7)).
        Reminder: Coordinates have to be translated!

    Example:
        >>> board = Board()
        >>> board.board = board.empty_board()
        >>> print(board.show())
        ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ 
        ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
        ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
        ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
        ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
        ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
        ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
        ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡

    Returns:
        list: Nested list of Entitys that represents the chess board.
    """
    board = []

    for i in range(8):
        board.append([Empty((j, i)) for j in range(8)])

    return board


class Boundary:
    """Class that is used to check if a value is in a boundary.

    Args:
        min (int): Minimal value inside boundary.
        max (int): Exclusive max value inside boundary.

    Example:
        >>> boundary = Boundary(0, 4)
        >>> boundary.accepts(0)
        True
        >>> boundary.accepts(4)
        False
    """
    def __init__(self, min: int, max: int):
        self.__min = min
        self.__max = max
    
    def accepts(self, value: Union[int, Tuple[int]]) -> bool:
        """Check if the value is inside the boundary.

        Args:
            value (int) value that shall be checked

        Returns:
            boolean: True if value is in boundary, False otherwise.
        
        Example:
        >>> boundary = Boundary(0, 4)
        >>> boundary.accepts(0)
        True
        >>> boundary.accepts((0, 0))
        True
        >>> boundary.accepts(4)
        False
        """
        if isinstance(value, int):
            value = tuple(value)

        in_boundary = [v in range(self.__min, self.__max) for v in value]

        return all(in_boundary)


def coord_to_json(coord: Union[List[Tuple[int, int]], Tuple[int, int]],
                  as_list: bool = False) -> dict:
    """Convert a coordinate into a JSON representation."""
    if isinstance(coord, tuple):
        coord = [coord]

    json = []
    for x, y in coord:
        json.append({"x": x, "y": y})

    if len(json) == 1 and not as_list:
        return json[0]

    return json


def json_to_coord(json: dict, as_list: bool = False) -> Union[List[Tuple[int, int]], Tuple[int, int]]:
    """Convert a coordinate in JSON representation into the internal."""
    if isinstance(json, dict):
        json = [json]

    coord = []
    for i in json:
        x, y = i["x"], i["y"]
        coord.append((x, y))

    if len(coord) == 1 and not as_list:
        return coord[0]

    return coord


def normalize(x: int) -> int:
    """Normalize an integer between -1 and 1."""
    if x > 0:
        return 1
    elif x < 0:
            return -1
    return 0


def str_to_piece(self, type: str, coord: Tuple[int], player: str, whitelist: Union[None, set] = None) -> Type[Piece]:
    """Return a piece via it's type and other params.

    Args:
        type (str): Name of the class of the `Piece` object. 
        coord (:obj:`tuple` of :obj:`int`): Coordinate of the piece on board.
        player (str): Name of the piece's player.
        whitelist (:obj:`set` of str): Whitelist for piece types.

    Returns:
        piece: A default piece object of given type and coord as well as player.

    Raises:
        NotWhitelistedException: The given piece type is not whitelisted!
    """
    if whitelist and type not in whitelist:
        raise NotWhitelistedException(f"The given piece type is not whitelisted! {type} not in {whitelist}")

    switch = {"Pawn": Pawn, "Knight": Knight, "Bishop": Bishop,
              "Rook": Rook, "Queen": Queen, "King": King}

    return switch[type](coord, player)