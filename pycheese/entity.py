# -*- coding: utf-8 -*-
"""Entities that populate a chess board.

This module contains code that represents the entities
of a chessboard in an object-oriented style.

Example:
    >>> queen = Queen(cord, member, moves)
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
        cord (:obj:`tuple` of :obj:`int`): Coordinate of the entity on the chessboard.
        attacked (bool): Boolean that states if this entity is attacked.
        attacker (:obj:`Piece`): Piece that is attacking this entity.
        pinned (bool): Boolean that states if this entity is pinned by an attacker.
    """
    def __init__(self, cord: Tuple[int, int]):

        self.cord = cord

        self.attacked = False
        self.attacker = None
        self.pinned = False

    def set_attacked(self, status: bool) -> None:
        """Sets the entity's attacked attribute to the specified status."""
        self.attacked = status

    def is_attacked(self) -> bool:
        """Get the value of the entity's attacked attribute."""
        return self.attacked

    def set_pinned(self, status: bool, attacker: Entity = None) -> None:
        """
        Set this entity's pinned attribute.

        Args:
            status (bool): Value the pinned attribute is to be set.
            attacker (:obj:`Piece`, optional): Piece that is causing the pinn. 
        """
        self.pinned = status
        self.attacker = attacker
    
    def is_pinned(self) -> tuple[bool, Union[Piece, None]]:
        return self.pinned, self.attacker


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
        member (str): Name of the player ("white" or "black").
        moves (:obj:`tuple` of :obj:`tuple` of int): Piece`s set of valid moves.

    Attributes:
        member (str): Name of the player ("white" or "black").
        moves (:obj:`tuple` of :obj:`tuple` of int): Piece`s set of valid moves.
    """
    def __init__(self, cord: Tuple[int, int], member: str, moves: Tuple[Tuple[int, int]]):
        super().__init__(cord)
        
        self.member = member
        self.moves = moves

    def get_moves(self) -> Tuple[Tuple[int, int]]:
        """Get all theoretical moves of the piece."""
        return self.moves

    def membership(self) -> str:
        """Get the membership attribute of the piece."""
        return self.member

    def set_cord(self, cord: Tuple[int, int]) -> None:
        """Set the coordinate of the piece."""
        self.cord = cord

    def get_cord(self) -> Tuple[int, int]:
        """Get the coordinate of the piece."""
        return self.cord


class Pawn(Piece):
    """Object-oriented representation of a pawn.

    Note:
        Pawns have an special set of moves that are not given to the abstract class.

    Args:
        cord (:obj:`tuple` of :obj:`int`): Coordinate of the entity on the chessboard.
        member (str): Name of the player ("white" or "black").

    Attributes:
        moves (:obj:`tuple` of :obj:`tuple` of int): Subset set of a pawns valid moves.
        attack_moves (:obj:`tuple` of :obj:`tuple` of int): Set of valid attacking moves.
        special_move (:obj:`tuple` of int): Pawn`s special move (2^ from start).
        start_cord (:obj:`tuple` of int): The pawns starting position on the chessboard.

    Example:
        >>> pawn = Pawn(cord, member)
        >>> assert isinstance(pawn, Piece)
        >>> assert isinstance(pawn, Entity)
    """
    moves = ((0, 1),)
    attack_moves = ((-1, 1), (1, 1))
    special_move = (0, 2)

    def __init__(self, cord: Tuple[int, int], member: str):
        super().__init__(cord, member, Pawn.moves)

        self.start_cord = cord

        self.attack_moves = Pawn.attack_moves
        self.special_move = Pawn.special_move
    
    def get_attack_moves(self) -> Tuple[Tuple[int, int]]:
        """Get all moves a pawn can use to attack entities."""
        return self.attack_moves

    def can_special(self) -> bool:
        """Get a boolean that states if a pawn moves 2 squares down the board."""
        return self.start_cord == self.cord

    def get_special_move(self) -> Tuple[Tuple[int, int]]:
        """Get a pawns special move."""
        return self.special_move

    def __str__(self) -> str:
        """Get the string representation of the pawn."""
        return "♙" if self.member == "white" else "♟︎"


class Knight(Piece):
    """Object-oriented represenation of a knight.

    Args:
        cord (:obj:`tuple` of :obj:`int`): Coordinate of the entity on the chessboard.
        member (str): Name of the player ("white" or "black").

    Attributes:
        moves (:obj:`tuple` of :obj:`tuple` of int): Subset set of a pawns valid moves.

    Example:
        >>> knight = Knight(cord, member)
        >>> assert isinstance(pawn, Piece)
        >>> assert isinstance(pawn, Entity)
    """
    moves = ((-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1))

    def __init__(self, cord: Tuple[int, int], member: str):
        super().__init__(cord, member, Knight.moves)

    def __str__(self) -> str:
        """Get the string representation of the knight."""
        return "♘" if self.member == "white" else "♞"


class Bishop(Piece):
    """Object-oriented represenation of a bishop.

    Args:
        cord (:obj:`tuple` of :obj:`int`): Coordinate of the entity on the chessboard.
        member (str): Name of the player ("white" or "black").

    Attributes:
        moves (:obj:`tuple` of :obj:`tuple` of int): Subset set of a pawns valid moves.

    Example:
        >>> knight = Knight(cord, member)
        >>> assert isinstance(pawn, Piece)
        >>> assert isinstance(pawn, Entity)
    """
    moves = ((-1, 1), (1, 1), (1, -1), (-1, -1))

    def __init__(self, cord: Tuple[int, int], member: str):
        super().__init__(cord, member, Bishop.moves)

    def __str__(self) -> str:
        """Get the string representation of the bishop."""
        return "♗" if self.member == "white" else "♝"

class Rook(Piece):
    """Object-oriented represenation of a rook.

    Args:
        cord (:obj:`tuple` of :obj:`int`): Coordinate of the entity on the chessboard.
        member (str): Name of the player ("white" or "black").

    Attributes:
        moves (:obj:`tuple` of :obj:`tuple` of int): Subset set of a pawns valid moves.
        moved (bool): States if the rook has already moved.

    Example:
        >>> rook = Rook(cord, member)
        >>> assert isinstance(pawn, Piece)
        >>> assert isinstance(pawn, Entity)
    """
    moves = ((0, 1), (1, 0), (0, -1), (-1, 0))

    def __init__(self, cord: Tuple[int, int], member: str):
        super().__init__(cord, member, Rook.moves)

        self.moved = False
    
    def did_move(self) -> None:
        """Set moved attribute of the rook to True."""
        self.moved = True

    def has_moved(self) -> bool:
        """Get moved attribute of the rook."""
        return self.moved

    def __str__(self) -> str:
        """Get the string representation of the rook."""
        return "♖" if self.member == "white" else "♜"

class Queen(Piece):
    """Object-oriented represenation of a queen.

    Args:
        cord (:obj:`tuple` of :obj:`int`): Coordinate of the entity on the chessboard.
        member (str): Name of the player ("white" or "black").

    Attributes:
        moves (:obj:`tuple` of :obj:`tuple` of int): Subset set of a pawns valid moves.
        moved (bool): States if the rook has already moved.

    Example:
        >>> queen = Queen(cord, member)
        >>> assert isinstance(pawn, Piece)
        >>> assert isinstance(pawn, Entity)
    """
    moves = ((0, 1), (1, 0), (0, -1), (-1, 0), (-1, 1), (1, 1), (1, -1), (-1, -1))

    def __init__(self, cord: Tuple[int, int], member: str):
        super().__init__(cord, member, Queen.moves)

    def __str__(self) -> str:
        """Get the string representation of the queen."""
        return "♕" if self.member == "white" else "♛"

class King(Piece):
    """Object oriented represenation of a king.

    Args:
        cord (:obj:`tuple` of :obj:`int`): Coordinate of the entity on the chessboard.
        member (str): Name of the player ("white" or "black").

    Attributes:
        moves (:obj:`tuple` of :obj:`tuple` of int): Subset set of a pawns valid moves.
        moved (bool): States if the king has already moved.

    Example:
        >>> king = King(cord, member)
        >>> assert isinstance(pawn, Piece)
        >>> assert isinstance(pawn, Entity)
    """
    moves = ((0, 1), (1, 0), (0, -1), (-1, 0), (-1, 1), (1, 1), (1, -1), (-1, -1))

    def __init__(self, cord: Tuple[int, int], member: str):
        super().__init__(cord, member, King.moves)

        self.moved = False
    
    def did_move(self) -> None:
        """Set moved attribute of the king to True."""
        self.moved = True

    def has_moved(self) -> bool:
        """Get moved attribute of the rook."""
        return self.moved

    def __str__(self) -> str:
        """Get the string representation of the king."""
        return "♔" if self.member == "white" else "♚"
        


