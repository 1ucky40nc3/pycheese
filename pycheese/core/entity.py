# -*- coding: utf-8 -*-
"""Entities that populate a chess board.

This module contains code that represents the entities
of a chessboard in an object-oriented style.

Example:
    >>> queen = Queen(cord, player, moves)
    >>> assert  isinstance(queen, Piece)
    >>> assert  isinstance(queen, Entity)
"""


from __future__ import annotations

from typing import Type
from typing import Union
from typing import Tuple


class Entity:
    """Abstact class for entities an a chessboard.
    
    Args:
        cord (:obj:`tuple` of :obj:`int`): Coordinate of the entity on the chessboard.

    Attributes:
        __cord (:obj:`tuple` of :obj:`int`): Coordinate of the entity on the chessboard.
    """
    def __init__(self, cord: Tuple[int, int]):
        self.__cord = cord

    def set_cord(self, cord: Tuple[int, int]) -> None:
        """Set the coordinate of the piece."""
        self.__cord = cord

    def get_cord(self) -> Tuple[int, int]:
        """Get the coordinate of the piece."""
        return self.__cord

class Empty(Entity):
    """A class that represents empty squares on a chessboard.
    
    Args:
        cord (:obj:`tuple` of :obj:`int`): Coordinate of the entity on the chessboard.
    
    Example:
        >>> empty = Empty(cord)
        >>> assert isinstance(empty, Entity)
    """
    def __init__(self, cord: Tuple[int, int]):
        super().__init__(cord)

    def __str__(self) -> str:
        """Get the string representation of an empty field (⊡)."""
        return "⊡"


class Piece(Entity):
    """Abstract class that represents a non-empty square on the chessboard.
    
    This means a piece could be a Pawn, Knight, Bishop, Rook, Queen or King.

    Args:
        cord (:obj:`tuple` of :obj:`int`): Coordinate of the entity on the chessboard.
        player (str): Name of the player ("white" or "black").
        moves (:obj:`tuple` of :obj:`tuple` of int): Piece`s set of valid moves.

    Attributes:
        __player (str): Name of the player ("white" or "black").
        __moves (:obj:`tuple` of :obj:`tuple` of int): Piece`s set of valid moves.
        __attacked (bool): Boolean that states if this entity is attacked.
        __attacker (:obj:`Piece`): Piece that is attacking this entity.
        __pinned (bool): Boolean that states if this entity is pinned by an attacker.
    """
    def __init__(self, cord: Tuple[int, int], player: str, moves: Tuple[Tuple[int, int]]):
        super().__init__(cord)
        
        self.__player = player
        self.__moves = moves

        self.__attacked = False
        self.__attacker = None
        self.__pinned = False

    def get_moves(self) -> Tuple[Tuple[int, int]]:
        """Get all theoretical moves of the piece."""
        return self.__moves

    def get_player(self) -> str:
        """Get the playership attribute of the piece."""
        return self.__player

    def set_attacked(self, status: bool) -> None:
        """Sets the entity's attacked attribute to the specified status."""
        self.__attacked = status

    def is_attacked(self) -> bool:
        """Get the value of the entity's attacked attribute."""
        return self.__attacked

    def set_pinned(self, status: bool) -> None:
        """Set this pieces's pinned attribute."""
        self.__pinned = status
    
    def is_pinned(self) -> tuple[bool]:
        """Get if the piece is pinned."""
        return self.__pinned

    def set_attacker(self, attacker: Union[Type[Piece], None] = None) -> None:
        """Set the piece's attacker."""
        self.__attacker = attacker

    def get_attacker(self) -> Union[Type[Piece], None]:
        """Get if the piece's attacker."""
        return self.__attacker


class Pawn(Piece):
    """Object-oriented representation of a pawn.

    Note:
        Pawns have an special set of moves that are not given to the abstract class.

    Args:
        cord (:obj:`tuple` of :obj:`int`): Coordinate of the entity on the chessboard.
        player (str): Name of the player ("white" or "black").

    Attributes:
        moves (:obj:`tuple` of :obj:`tuple` of int): Subset set of a pawns valid moves.
        attack_moves (:obj:`tuple` of :obj:`tuple` of int): Set of valid attacking moves.
        special_move (:obj:`tuple` of int): Pawn`s special move (2^ from start).
        __start_cord (:obj:`tuple` of int): The pawns starting position on the chessboard.

    Example:
        >>> pawn = Pawn(cord, player)
        >>> assert isinstance(pawn, Piece)
        >>> assert isinstance(pawn, Entity)
    """
    moves: Tuple[Tuple[int, int]] = ((0, 1),)

    attack_moves: Tuple[Tuple[int, int]] = ((-1, 1), (1, 1))
    special_move: Tuple[Tuple[int, int]] = (0, 2)

    def __init__(self, cord: Tuple[int, int], player: str):
        super().__init__(cord, player, Pawn.moves)

        self.__start_cord = cord
    
    def get_attack_moves(self) -> Tuple[Tuple[int, int]]:
        """Get all moves a pawn can use to attack entities."""
        return Pawn.attack_moves

    def can_special(self) -> bool:
        """Get a boolean that states if a pawn moves 2 squares down the board."""
        return self.__start_cord == self.__cord

    def get_special_move(self) -> Tuple[Tuple[int, int]]:
        """Get a pawns special move."""
        return Pawn.special_move

    def __str__(self) -> str:
        """Get the string representation of the pawn."""
        return "♙" if self.__player == "white" else "♟︎"


class Knight(Piece):
    """Object-oriented represenation of a knight.

    Args:
        cord (:obj:`tuple` of :obj:`int`): Coordinate of the entity on the chessboard.
        player (str): Name of the player ("white" or "black").

    Attributes:
        moves (:obj:`tuple` of :obj:`tuple` of int): Subset set of a pawns valid moves.

    Example:
        >>> knight = Knight(cord, player)
        >>> assert isinstance(pawn, Piece)
        >>> assert isinstance(pawn, Entity)
    """
    moves: Tuple[Tuple[int, int]] = (
        (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1))

    def __init__(self, cord: Tuple[int, int], player: str):
        super().__init__(cord, player, Knight.moves)

    def __str__(self) -> str:
        """Get the string representation of the knight."""
        return "♘" if self.__player == "white" else "♞"


class Bishop(Piece):
    """Object-oriented represenation of a bishop.

    Args:
        cord (:obj:`tuple` of :obj:`int`): Coordinate of the entity on the chessboard.
        player (str): Name of the player ("white" or "black").

    Attributes:
        moves (:obj:`tuple` of :obj:`tuple` of int): Subset set of a pawns valid moves.

    Example:
        >>> knight = Knight(cord, player)
        >>> assert isinstance(pawn, Piece)
        >>> assert isinstance(pawn, Entity)
    """
    moves: Tuple[Tuple[int, int]] = ((-1, 1), (1, 1), (1, -1), (-1, -1))

    def __init__(self, cord: Tuple[int, int], player: str):
        super().__init__(cord, player, Bishop.moves)

    def __str__(self) -> str:
        """Get the string representation of the bishop."""
        return "♗" if self.__player == "white" else "♝"

class Rook(Piece):
    """Object-oriented represenation of a rook.

    Args:
        cord (:obj:`tuple` of :obj:`int`): Coordinate of the entity on the chessboard.
        player (str): Name of the player ("white" or "black").

    Attributes:
        moves (:obj:`tuple` of :obj:`tuple` of int): Subset set of a pawns valid moves.
        __moved (bool): States if the rook has already moved.

    Example:
        >>> rook = Rook(cord, player)
        >>> assert isinstance(pawn, Piece)
        >>> assert isinstance(pawn, Entity)
    """
    moves: Tuple[Tuple[int, int]] = ((0, 1), (1, 0), (0, -1), (-1, 0))

    def __init__(self, cord: Tuple[int, int], player: str):
        super().__init__(cord, player, Rook.moves)

        self.__moved = False
    
    def did_move(self) -> None:
        """Set moved attribute of the rook to True."""
        self.__moved = True

    def get_moved(self) -> bool:
        """Get moved attribute of the rook."""
        return self.__moved

    def __str__(self) -> str:
        """Get the string representation of the rook."""
        return "♖" if self.__player == "white" else "♜"

class Queen(Piece):
    """Object-oriented represenation of a queen.

    Args:
        cord (:obj:`tuple` of :obj:`int`): Coordinate of the entity on the chessboard.
        player (str): Name of the player ("white" or "black").

    Attributes:
        moves (:obj:`tuple` of :obj:`tuple` of int): Subset set of a pawns valid moves.

    Example:
        >>> queen = Queen(cord, player)
        >>> assert isinstance(pawn, Piece)
        >>> assert isinstance(pawn, Entity)
    """
    moves: Tuple[Tuple[int, int]] = (
        (0, 1), (1, 0), (0, -1), (-1, 0), (-1, 1), (1, 1), (1, -1), (-1, -1))

    def __init__(self, cord: Tuple[int, int], player: str):
        super().__init__(cord, player, Queen.moves)

    def __str__(self) -> str:
        """Get the string representation of the queen."""
        return "♕" if self.__player == "white" else "♛"

class King(Piece):
    """Object oriented represenation of a king.

    Args:
        cord (:obj:`tuple` of :obj:`int`): Coordinate of the entity on the chessboard.
        player (str): Name of the player ("white" or "black").

    Attributes:
        moves (:obj:`tuple` of :obj:`tuple` of int): Subset set of a pawns valid moves.
        __moved (bool): States if the king has already moved.

    Example:
        >>> king = King(cord, player)
        >>> assert isinstance(pawn, Piece)
        >>> assert isinstance(pawn, Entity)
    """
    moves: Tuple[Tuple[int, int]] = (
        (0, 1), (1, 0), (0, -1), (-1, 0), (-1, 1), (1, 1), (1, -1), (-1, -1))

    def __init__(self, cord: Tuple[int, int], player: str):
        super().__init__(cord, player, King.moves)

        self.__moved = False
    
    def did_move(self) -> None:
        """Set moved attribute of the king to True."""
        self.__moved = True

    def get_moved(self) -> bool:
        """Get moved attribute of the rook."""
        return self.__moved

    def __str__(self) -> str:
        """Get the string representation of the king."""
        return "♔" if self.__player == "white" else "♚"