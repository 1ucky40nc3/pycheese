# -*- coding: utf-8 -*-
"""Entities that populate a chess board.

This module contains code that represents the entities
of a chessboard in an object-oriented style.

Example:
    >>> queen = Queen(coord, player, moves)
    >>> assert  isinstance(queen, Piece)
    >>> assert  isinstance(queen, Entity)
"""


from __future__ import annotations

from typing import Optional

from pycheese.core.utils import coord_to_dict


class Entity:
    """Abstact class for entities an a chessboard.
    
    Args:
        coord (`list` of `int`): Coordinate of the entity on the chessboard.

    Attributes:
        __coord (`list` of `int`): Coordinate of the entity on the chessboard.
        __attacked (bool): Boolean that states if this entity is attacked.
    """
    def __init__(self, coord: list[int, int]):
        self.__coord = coord
        self.__attacked = False

    def set_coord(self, coord: list[int, int]) -> None:
        """Set the coordinate of the piece."""
        self.__coord = coord

    def get_coord(self) -> list[int, int]:
        """Get the coordinate of the piece."""
        return self.__coord

    def set_attacked(self, status: bool) -> None:
        """Sets the entity's attacked attribute to the specified status."""
        self.__attacked = status

    def is_attacked(self) -> bool:
        """Get the value of the entity's attacked attribute."""
        return self.__attacked

    def __eq__(self, other: Entity):
        """Check two entities for equallity."""
        return (self.__class__ == other.__class__ and
                self.get_coord() == other.get_coord())

class Empty(Entity):
    """A class that represents empty squares on a chessboard.
    
    Args:
        coord (`list` of `int`): Coordinate of the entity on the chessboard.
    
    Example:
        >>> empty = Empty(coord)
        >>> assert isinstance(empty, Entity)
    """
    def __init__(self, coord: list[int, int]):
        super().__init__(coord)

    def __str__(self) -> str:
        """Get the string representation of an empty field (⊡)."""
        return "⊡"


class Piece(Entity):
    """Abstract class that represents a non-empty square on the chessboard.
    
    This means a piece could be a Pawn, Knight, Bishop, Rook, Queen or King.

    Args:
        coord (`list` of `int`): Coordinate of the entity on the chessboard.
        player (`str`): Name of the player ("white" or "black").
        moves (`list` of `list` of int): Piece`s set of valid moves.

    Attributes:
        __player (`str`): Name of the player ("white" or "black").
        __moves (`list` of `list` of int): Piece`s set of valid moves.
        __options (`dict`):  Piece`s options on the board. With a shape of {"moves": ..., "other": ...}
        __pinned (`bool`): Boolean that states if this entity is pinned by an attacker.
        __attacker (`Piece`): Piece that is attacking this entity by it's coord.
    """
    def __init__(self, coord: list[int, int], player: str, moves: list[list[int, int]]):
        super().__init__(coord)
        
        self.__player = player
        self.__moves = moves
        self.__options = {"moves": [], "others": []}

        self.__pinned = False
        self.__pinner = None

    def get_moves(self) -> list[list[int, int]]:
        """Get all theoretical moves of the piece."""
        return self.__moves

    def get_player(self) -> str:
        """Get the player attribute of the piece."""
        return self.__player

    def set_options(self, options: dict):
        """Set the current options of the piece on the board."""
        self.__options = options

    def get_options(self) -> dict:
        """Set the current options of the piece on the board."""
        return self.__options

    def set_pinned(self, status: bool) -> None:
        """Set this pieces's pinned attribute."""
        self.__pinned = status
    
    def is_pinned(self) -> list[bool]:
        """Get if the piece is pinned."""
        return self.__pinned

    def set_pinner(self, pinner: Optional[list[int]] = None) -> None:
        """Set the piece's attacker."""
        self.__pinner = pinner

    def get_pinner(self) -> Optional[list[int]]:
        """Get if the piece's attacker."""
        return self.__pinner

    def __hash__(self) -> int:
        """Get the hash value of this object."""
        return hash((
            self.__class__.__name__,
            self.get_player(),
            self.get_coord(),
        ))

    def to_dict(self) -> dict:
        """Return a JSON representation of this objects data."""
        # Convert the coordinate into a JSON object.
        coord = coord_to_dict(self.get_coord())

        # Convert the piece's options to JSON.
        options = self.get_options()
        if options:
            moves = coord_to_dict(
                options["moves"], as_list=True)

            others = options["others"]
            for i in range(len(others)):
                companion = others[i]["companion"]
                cmove = others[i]["cmove"]
                pmove = others[i]["pmove"]

                others[i] = {
                    "companion": coord_to_dict(companion),
                    "cmove": coord_to_dict(cmove),
                    "pmove": coord_to_dict(pmove)
                }

        # Represent the attacker via it's coordinate 
        # on the board, if the attacker exists.
        pinner = self.get_pinner()

        if pinner:
            pinner = coord_to_dict(pinner)

        return {
            "type": self.__class__.__name__,
            "player": self.get_player(),
            "coord": coord,
            "options": options,
            "pinned": self.is_pinned(),
            "pinner": pinner,
        }


class Pawn(Piece):
    """Object-oriented representation of a pawn.

    Note:
        Pawns have an special set of moves that are not given to the abstract class.

    Args:
        coord (`list` of `int`): Coordinate of the entity on the chessboard.
        player (`str`): Name of the player ("white" or "black").

    Attributes:
        moves (`list` of `list` of `int`): Subset set of a pawns valid moves.
        attack_moves (`list` of `list` of `int`): Set of valid attacking moves.
        special_move (`list` of `int`): Pawn`s special move (2^ from start).
        __start_coord (`list` of `int`): The pawns starting position on the chessboard.

    Example:
        >>> pawn = Pawn(coord, player)
        >>> assert isinstance(pawn, Piece)
        >>> assert isinstance(pawn, Entity)
    """
    moves: list[list[int, int]] = [[0, 1]]

    attack_moves: list[list[int, int]] = [[-1, 1], [1, 1]]
    special_move: list[int, int] = [0, 2]

    def __init__(self, coord: list[int, int], player: str):
        super().__init__(coord, player, Pawn.moves)

        self.__start_coord = coord
    
    def get_attack_moves(self) -> list[list[int, int]]:
        """Get all moves a pawn can use to attack entities."""
        return Pawn.attack_moves

    def can_special(self) -> bool:
        """Get a boolean that states if a pawn moves 2 squares down the board."""
        return self.__start_coord == self.get_coord()

    def get_special_move(self) -> list[list[int, int]]:
        """Get a pawns special move."""
        return Pawn.special_move

    def __str__(self) -> str:
        """Get the string representation of the pawn."""
        return "♙" if self.get_player() == "white" else "♟︎"


class Knight(Piece):
    """Object-oriented represenation of a knight.

    Args:
        coord (`list` of `int`): Coordinate of the entity on the chessboard.
        player (`str`): Name of the player ("white" or "black").

    Attributes:
        moves (`list` of `list` of `int`): Subset set of a pawns valid moves.

    Example:
        >>> knight = Knight(coord, player)
        >>> assert isinstance(pawn, Piece)
        >>> assert isinstance(pawn, Entity)
    """
    moves: list[list[int, int]] = [
        [-1, 2], [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1]]

    def __init__(self, coord: list[int, int], player: str):
        super().__init__(coord, player, Knight.moves)

    def __str__(self) -> str:
        """Get the string representation of the knight."""
        return "♘" if self.get_player() == "white" else "♞"


class Bishop(Piece):
    """Object-oriented represenation of a bishop.

    Args:
        coord (`list` of `int`): Coordinate of the entity on the chessboard.
        player (`str`): Name of the player ("white" or "black").

    Attributes:
        moves (`list` of `list` of int): Subset set of a pawns valid moves.

    Example:
        >>> knight = Knight(coord, player)
        >>> assert isinstance(pawn, Piece)
        >>> assert isinstance(pawn, Entity)
    """
    moves: list[list[int, int]] = [[-1, 1], [1, 1], [1, -1], [-1, -1]]

    def __init__(self, coord: list[int, int], player: str):
        super().__init__(coord, player, Bishop.moves)

    def __str__(self) -> str:
        """Get the string representation of the bishop."""
        return "♗" if self.get_player() == "white" else "♝"

class Rook(Piece):
    """Object-oriented represenation of a rook.

    Args:
        coord (`list` of `int`): Coordinate of the entity on the chessboard.
        player (`str`): Name of the player ("white" or "black").

    Attributes:
        moves (`list` of `list` of `int`): Subset set of a pawns valid moves.
        __moved (`bool`): States if the rook has already moved.

    Example:
        >>> rook = Rook(coord, player)
        >>> assert isinstance(pawn, Piece)
        >>> assert isinstance(pawn, Entity)
    """
    moves: list[list[int, int]] = [[0, 1], [1, 0], [0, -1], [-1, 0]]

    def __init__(self, coord: list[int, int], player: str):
        super().__init__(coord, player, Rook.moves)

        self.__moved = False
    
    def did_move(self) -> None:
        """Set moved attribute of the rook to True."""
        self.__moved = True

    def get_moved(self) -> bool:
        """Get moved attribute of the rook."""
        return self.__moved

    def __str__(self) -> str:
        """Get the string representation of the rook."""
        return "♖" if self.get_player() == "white" else "♜"

class Queen(Piece):
    """Object-oriented represenation of a queen.

    Args:
        coord (`list` of `int`): Coordinate of the entity on the chessboard.
        player (`str`): Name of the player ("white" or "black").

    Attributes:
        moves (`list` of `list` of `int`): Subset set of a pawns valid moves.

    Example:
        >>> queen = Queen(coord, player)
        >>> assert isinstance(pawn, Piece)
        >>> assert isinstance(pawn, Entity)
    """
    moves: list[list[int, int]] = [
        [0, 1], [1, 0], [0, -1], [-1, 0], [-1, 1], [1, 1], [1, -1], [-1, -1]]

    def __init__(self, coord: list[int, int], player: str):
        super().__init__(coord, player, Queen.moves)

    def __str__(self) -> str:
        """Get the string representation of the queen."""
        return "♕" if self.get_player() == "white" else "♛"

class King(Piece):
    """Object oriented represenation of a king.

    Args:
        coord (`list` of `int`): Coordinate of the entity on the chessboard.
        player (`str`): Name of the player ("white" or "black").

    Attributes:
        moves (`list` of `list` of `int`): Subset set of a pawns valid moves.
        __moved (bool): States if the king has already moved.

    Example:
        >>> king = King(coord, player)
        >>> assert isinstance(pawn, Piece)
        >>> assert isinstance(pawn, Entity)
    """
    moves: list[list[int, int]] = [
        [0, 1], [1, 0], [0, -1], [-1, 0], [-1, 1], [1, 1], [1, -1], [-1, -1]]

    def __init__(self, coord: list[int, int], player: str):
        super().__init__(coord, player, King.moves)

        self.__moved = False
    
    def did_move(self) -> None:
        """Set moved attribute of the king to True."""
        self.__moved = True

    def get_moved(self) -> bool:
        """Get moved attribute of the rook."""
        return self.__moved

    def __str__(self) -> str:
        """Get the string representation of the king."""
        return "♔" if self.get_player() == "white" else "♚"