# -*- coding: utf-8 -*-
"""Objec-oriented representation of a chessboard.

This module contains code that represents
a chessboard in an object-oriented style.

Example:
    >>> board = Board()
    >>> board.show()
    ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ 
    ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ ♟︎
    ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
    ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
    ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
    ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
    ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙
    ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖
    >>> board.inspect([0, 6])
    {
        "coord": {
            "x": 0,
            "y": 6
        },
        "piece": {
            "type": "Pawn", 
            "player": "white", 
            "coord": {
                "x": 0, 
                "y": 6
            }, 
            "pinned": False, 
            "attacker": None
        },
        "moves": [
            {
                "x": 0, 
                "y": 5
            },
            {
                "x": 0, 
                "y": 4
            },
        ]
    }
    >>> board.move([0, 6], [0, 5])
    {
        "state": "ongoing",
        "source_coord": {
            "x": 0, 
            "y": 6,
        }
        "target_coord": {
            "x": 0, 
            "y": 5,
        }
        "event": {
            "type": None,
            "extra": None 
        }  
    }
    >>> board.show()
    ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ 
    ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ ♟︎
    ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
    ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
    ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
    ♙ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
    ⊡ ♙ ♙ ♙ ♙ ♙ ♙ ♙
    ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖
"""


from __future__ import annotations

import copy

from typing import Optional

from pycheese.core.entity import Entity
from pycheese.core.entity import Empty
from pycheese.core.entity import Piece
from pycheese.core.entity import Pawn
from pycheese.core.entity import Knight
from pycheese.core.entity import Bishop
from pycheese.core.entity import Rook
from pycheese.core.entity import Queen
from pycheese.core.entity import King

from pycheese.core.utils import Boundary
from pycheese.core.utils import coord_to_dict
from pycheese.core.utils import dict_to_coord
from pycheese.core.utils import normalize

from pycheese.core.error import NotInPlayersPossesionException
from pycheese.core.error import NoPieceAtSpecifiedCoordinateException
from pycheese.core.error import MoveNotLegalException
from pycheese.core.error import NotWhitelistedException


class Board:
    """Object-oriented representation of a chess board.

    Args:
        json (dict): A JSON representation of an objects this class produces.

    Attributes:
        state (str): State of the game (`ongoing`/`check`/`checkmate`/`stalemate`).
        player (str): String that identifies the player whose turn it is.
        board (`list` of `list` of `Entity`): list representing the board.
    """
    def __init__(self, json: Optional[dict] = None):
        self.state = "ongoing"
        self.player = "white"

        self.last = {}
        self.board = []
        self.init(json)

    def set(self, board: list[list[Entity]]) -> None:
        self.board = board

    def get(self) -> list[list[Entity]]:
        return self.board

    def init(self, json: Optional[dict]) -> None:
        """Initialize the Board classes board.
        
        Args:
            json (dict): A JSON representation of an objects this class produces.
        """
        if json:
            self.from_dict(json)
        else:
            self.set(initial_board())
            self.update()

    def move(self, source_coord: list[int, int], 
             target_coord: list[int, int],
             promotion_target: Optional[str] = None) -> dict:
        """Move the a current player's piece.

        Move the a current player's piece that is specified via a coordinate on
        the board (`source_coord`) to a target coordinate (`target_coord`).

        If the move from source to target is legal, it will be executed.

        If a pawn shall be promoted the `promotion_target` parameter must be specified.
        This parameter identifies the type of piece that shall be spawned at the
        `target_coord` coordinate on the chessboard. The pawn at the `source_coord`
        coordinate will be substituted with an entity of type `Empty`.

        Args:
            source_coord (str or `list` of `int`): Initial coordinate of entity on board.
            target_coord (str or `list` of `int`): Target coordinate of entity on board.
            promotion_target (str, optional): String that identifies piece to promote pawn into.

        Returns:
            dict: The boards state.
                  The output is shaped like:
                    {
                        "state": state,                  # The boards state.
                        "source_coord": source_coord,    # The source coordinate.
                        "target_coord": target_coord,    # The target coordinate.
                        "event": {                       # Object with details about an event.
                            "type": message,             # Type of an event.
                            "extra": extra               # Extra data about the event.
                        }  
                    }
        
        Raises:
            ValueError: If the source and target coordinate are equal or out of bounds.
            NotInPlayersPossesionException: The source coordinate isn't under the current players posession.
            MoveNotLegalException: The move from source to target is not legal.
            NoPieceAtSpecifiedCoordinateException: There is no piece at the coordinate.

        Example:
            >>> board = Board()
            >>> board.move([0, 6], [0, 5])
            {
                "state": "ongoing",
                "source_coord": {
                    "x": 0, 
                    "y": 6,
                }
                "target_coord": {
                    "x": 0, 
                    "y": 5,
                }
                "event": {
                    "type": None,
                    "extra": None 
                }  
            }

        
        Todo:
            # TODO: Implement draw by default.
            # TODO: Test behavior.
        """
        if target_coord == source_coord:
            raise ValueError(
                "The target coordinate can't be equal to the source coordinate!")
        
        sx, sy = source_coord
        tx, ty = target_coord

        boundary = Boundary(0, 8)

        if not (boundary.accepts((sx, sy))):
            raise ValueError(
                "The source coordinate is out of bounds: {}".format(source_coord))
        
        if not (boundary.accepts((tx, ty))):
            raise ValueError(
                "The target coordinate is out of bounds: {}".format(target_coord))

        # Construct JSON for the function output.
        event = {"type": None, "extra": None}
        
        source_entity = self.board[sy][sx]
        target_entity = self.board[ty][tx]

        if not isinstance(source_entity, Piece):
            raise NoPieceAtSpecifiedCoordinateException(
                "There is no piece at the specified coordinate. {}".format(source_coord))
        else:
            if source_entity.get_player() != self.player:
                raise NotInPlayersPossesionException(
                    "The piece at source coordinate is not in the current player's possesion!")
    
            source_moves, others = self.get_piece_options(source_entity)
            if target_coord not in source_moves:
                raise MoveNotLegalException(
                    "The move from the source coordinate to the target coordinate is not legal!")

            else:
                if others:
                    for element in others:
                        cx, cy = element["companion"]
                        companion = self.board[cy][cx]

                        x, y = element["cmove"]
                        pmove = element["pmove"]

                        if target_coord == pmove:
                            # Place ``Empty`` at the companions former coordinate.
                            self.board[cy][cx] = Empty([cx, cy])

                            # Place the `companion` at the new coordinate.
                            companion.set_coord([x, y])
                            self.board[y][x] = companion

                            # Place the `source_entity` at the new coordinate.
                            source_entity.set_coord([tx, ty])
                            self.board[ty][tx] = source_entity

                            # Place ``Empty`` at the king former coordinate. 
                            self.board[sy][sx] = Empty([sx, sy])

                            side = "queenside" if tx < 4 else "kingside" 
                            event = {"type": "castle", "extra": side}
                            break
                else:
                    if isinstance(source_entity, Pawn) and (ty == 0 or ty == 7) and isinstance(target_entity, Empty):
                        # Request promotion target if is None.
                        if promotion_target is None:
                            event = {"type": "missing_promotion_target", "extra": None}

                        self.board[ty][tx] = str_to_piece(
                            promotion_target, target_coord, self.player, whitelist={"Queen", "Rook", "Bishop", "Knight"})

                        event = {"type": "promotion", "extra": promotion_target}

                    else:
                        if isinstance(self.board[ty][tx], Piece):
                            event["type"] = "captures"
                        else:
                            event["type"] = "move"
                        
                        is_unique, overlapp = self.is_unique_move(target_coord, source_entity)
                        if is_unique:
                            event["extra"] = "unique"
                        else:
                            event["extra"] = "".join(filter(None, ["multiple", overlapp]))

                        source_entity.set_coord(target_coord)
                        self.board[ty][tx] = source_entity

                        if (isinstance(source_entity, (Rook, King))):
                            # TODO: Check if works!
                            source_entity.did_move()

                    self.board[sy][sx] = Empty([sx, sy])
                
                # Set up for next turn.
                self.last = coord_to_dict(target_coord)
                self.next_turn()
        
        return {
            "state": self.state, 
            "source_coord": coord_to_dict(source_coord), 
            "target_coord": coord_to_dict(target_coord),
            "event": event
        }

    def inspect(self, coord: list[int, int]) -> dict:
        """Inspect a piece's moves.

        Get the moves of a current player's piece
        that is identified via it's coordinate on the board.

        Args:
            coord (`list` of `int`): Coordinate on the chess board.

        Returns:
            `dict`: Dictionary that represents data about a pieces moves.

        Raises:
            ValueError: If the source and target coordinate are equal or out of bounds.
            NotInPlayersPossesionException: The source coordinate isn't under the current players posession.
            NoPieceAtSpecifiedCoordinateException: There is no piece at the coordinate.

        Example:
            >>> board = Board()
            >>> board.inspect([0, 6])
            {
                "coord": {
                    "x": 0,
                    "y": 6
                },
                "piece": {
                    "type": "Pawn", 
                    "player": "white", 
                    "coord": {
                        "x": 0, 
                        "y": 6
                    }, 
                    "pinned": False, 
                    "attacker": None
                },
                "moves": [
                    {
                        "x": 0, 
                        "y": 5
                    },
                    {
                        "x": 0, 
                        "y": 4
                    },
                ]
            }
        """
        x, y = coord

        # Check if the coordinate is on the chess board.
        boundary = Boundary(0, 8)
        if not (boundary.accepts((x, y))):
            raise ValueError(f"The piece coordinate is out of bounds: {coord}")

        entity = self.board[y][x]

        if isinstance(entity, Piece):
            if entity.get_player() != self.player:
                raise NotInPlayersPossesionException(
                    "The piece at source coordinate is not in the current player's possesion!")
    
            piece_moves, _ = self.get_piece_options(entity, find_others=False)

            return {
                "coord": coord_to_dict(coord),
                "piece": entity.to_dict(entity),
                "moves": coord_to_dict(piece_moves, as_list=True)
            }
        
        raise NoPieceAtSpecifiedCoordinateException(
                "There is no piece at the specified coordinate. {}".format(coord))

    def get_piece_options(self, piece: Piece, board: list[list[Entity]] = None,
                          find_others: bool = True, attacking: bool = False) -> list[list[int, int]]:
        """Find a pieces legal moves.

        Args:
            piece (`Piece`): A piece of the current player.
            find_other (`bool`, optional): States if information about companion moves shall be returned.
            attacking (`bool`, optional): States if only moves that attack enemy pieces shall be returned.
            board (`list` of `list` of `Entity`, optional): list representing a board.

        Returns:
            `list`: piece_moves and companion moves
                * piece_moves (`list` of `list` of int): 
                    list of coordinates that can be legally accessed by the piece.
                * others (`list` of `dict`):
                    list of dicts of data associated with other legal moves (e.g. for castling).
                    The dict inside the list are of shape:
                        {
                            "companion": `Piece`,
                            "others": `list` of `list` of `int`
                            "piece_moves": `list` of `list` of `int`
                        }

        Example:
            >>> board = Board()                # Initialize a new board.
            >>> piece = board.get()[6][0]      # Moves of white pawn on a1.
            >>> board.get_piece_options(piece) # Get the pieces options.
            ([[0, 5], [0, 4]], [])
        """
        moves = []
        others = []

        px, py = piece.get_coord()

        # If no `board` is specified select the position (`self.board`).
        if board is None:
            board = self.board

            # Return the piece's options if they are already known.
            if piece.get_options():
                options = piece.get_options()
                return options["moves"], options["others"]

        boundary = Boundary(0, 8)
        for dx, dy in piece.get_moves():

            # Invert the movement for white `pieces`, 
            # because of the way the board has ben initialized.
            if piece.get_player() == "white":
                dy *= -1

            x, y = px, py
            loop = True

            # Traverse the path given by the movement of the `piece` types
            # from the `piece` coordinate and recoord the coordinates
            # until another `piece` was found or the coordinate is out of bounds.
            # These recoorded coordinates are regarded as the legal moves.
            while loop and boundary.accepts((x + dx, y + dy)):
                x += dx
                y += dy

                entity = board[y][x]
                if isinstance(entity, Piece):
                    if attacking:
                        loop = False
                    else:
                        if self.is_other_player_piece(entity, piece):
                            loop = False
                        else:
                            break

                    # Check if the `piece` could check the enemy king
                    # if a enemy `piece` would move. Set this `piece` to `pinned`.
                    if not self.is_check() and isinstance(piece, (Bishop, Rook, Queen)): 
                        tmp_x, tmp_y = x, y

                        while boundary.accepts((tmp_x + dx, tmp_y + dy)):
                            tmp_x += dx
                            tmp_y += dy

                            tmp_entity = board[tmp_y][tmp_x]

                            if isinstance(tmp_entity, Piece):
                                if self.is_other_player_king(tmp_entity, piece):
                                    sx, sy = entity.get_coord()

                                    self.board[sy][sx].set_pinned(True)
                                    self.board[sy][sx].set_pinner(piece.get_coord())
                                break
                
                moves.append([x, y])
                
                # End the loop for `pieces` of type ``Pawn``, ``Knight`` or ``King``.
                if isinstance(piece, (Pawn, Knight, King)):
                    break

        if isinstance(piece, King) and not attacking:                
            def is_attacked(move):
                x, y = move
                return not board[y][x].is_attacked()
            
            moves = list(filter(is_attacked, moves))

        # Check if the `piece` is of type ``Pawn``
        # and can execute it's unique movement.
        if isinstance(piece, Pawn):
            amoves = []

            for move in piece.get_attack_moves():
                dx, dy = move

                # Invert the movement for white `pieces`, 
                # because of the way the board has ben initialized.
                if piece.get_player() == "white":
                    dy *= -1

                x, y = px + dx, py + dy

                if boundary.accepts((x, y)):
                    # Check if a `piece` is at the current coordinate.
                    entity = board[y][x]

                    # Add the coordinate to `attacking_moves` if
                    # a ``Piece`` of the enemy is at the coordinate.
                    if not attacking and isinstance(entity, Piece):
                        if self.is_other_player_piece(entity, piece):
                            amoves.append([x, y])
                    # Add the coordinate to `attacking_moves` regardless
                    # of the fact that a ``Piece`` is at the coordinate.
                    # Because all attacking moves are recoorded.
                    # Check only if a chess piece is in the opponent's possession.
                    elif attacking:
                        amoves.append([x, y])    

            # If only attacking moves shall be recoorded,
            # `piece_moves` equal `attacking_moves`.
            if attacking:
                moves = amoves

            # Else append the `attacking_moves` to `piece_moves`
            # and check if the ``Pawn`` can execute it's special move.
            else:
                moves += amoves

                if piece.can_special():
                    dx, dy = piece.get_special_move()

                    if piece.get_player() == "white":
                        dy *= -1

                    x, y = px + dx, py + dy
                    
                    # Check if all coord in the path to [x, y] are empty.
                    coords = [[x, y - int(dy/2)], [x, y]]

                    if all(isinstance(board[j][i], Empty) for i, j in coords):
                        moves.append([x, y])
        
        # Check if `piece` is `pinned`. If the `piece` is `pinned`
        # it can only move in the `attackers` direction.
        # To compute the legal moves keep the coordinates
        # in the `attackers` `line_of_attack`
        # (the attackers moves towards the king).
        if piece.is_pinned():
            ax, ay = piece.get_pinner()

            dx, dy = ax - px, ay - py
            dx, dy = normalize(dx), normalize(dy)

            start_x, stop_x = sorted([ax, px])
            xboundary = Boundary(start_x, stop_x)
            
            start_y, stop_y = sorted([ay, py])
            yboundary = Boundary(start_y, stop_y)

            x, y = px, py
            tmp = []
            while xboundary.accepts(x + dx) and yboundary.accepts(y + dy):
                x += dx
                y += dy

                tmp.append([x, y])
            
            moves = list(filter(lambda move: move in tmp, moves))

        # If the current player is in check: Find all moves that resolve the check.
        if self.is_check() and not attacking:
            # If the `piece` is of type ``King`` then only moves
            # that lead to non attacked coordinates are valid.
            if isinstance(piece, King):
                ax, ay = dict_to_coord(self.last)
                entity = board[ay][ax]
                emoves = []
                
                boundary = Boundary(0, 8)
                for dx, dy in entity.get_moves():

                    x, y = ax, ay
                    while boundary.accepts((x + dx, y + dy)):
                        x += dx
                        y += dy

                        entity = board[y][x]
                        if isinstance(entity, Empty) or entity == piece:
                            emoves.append([x, y])
                        else:
                            break

                moves = list(filter(lambda move: move not in emoves, moves))

            # Else find the king and all moves of the
            # `piece` that hide the king from check.
            else:
                king = self.get_player_king()

                # List of all moves to avoid check.
                tmp = []

                # Set the `state` temporary to "ongoing" to look
                # into future positions without restrictions.
                self.state = "ongoing"

                # To block check the `piece` has to step into
                # squares on the board that are being attacked by the enemy.
                # Compute theese and check if the king is hidden from check.
                other_player_options = self.get_other_player_options(
                    include_piece_coord=True)

                for move in moves:
                    if move in other_player_options:
                        tmp_board = copy.deepcopy(board)
                        tmp_piece = copy.deepcopy(piece)

                        x, y = move
                        tmp_piece.set_coord([x, y])
                        tmp_board[y][x] = tmp_piece
                        tmp_board[py][px] = Empty([px, py])

                        if king.get_coord() not in self.get_other_player_options(board=tmp_board, save=False):
                            tmp.append([x, y])

                self.state = "check"
                moves = tmp

        # Check if the player can castle.
        # To so first check if the king has already moved or a given rook
        # who is identified by the side the `target_coord` leads to.
        # Afterwards check if the enemy is attacking squares that
        # are needed for castling or if theese squares are.
        if self.can_player_castle(piece, find_others, attacking):
            # Check if king has already moved.
            if not piece.get_moved():
                for step in range(-1, 2, 2):
                    cx = 0 if step == -1 else 7
                    companion = board[py][cx]

                    # Check if the `companion` of type `Rook` has already moved.
                    if (isinstance(companion, Rook) and not companion.get_moved()):
                        # Check for obstructed or attacked squares. 
                        path_not_obstructed = True

                        start, stop = (5, 7) if step == 1 else (1, 4)

                        for x in range(start, stop):
                            entity = board[py][x]

                            if isinstance(entity, Piece) or entity.is_attacked():
                                path_not_obstructed = False
                                break

                        if path_not_obstructed:
                            mx, my = px + step * 2, py
                            moves.append([mx, my])
                            
                            # TODO: Update comments that reference companion as `Piece`.
                            others.append({
                                "companion": companion.get_coord(),
                                "cmove": [mx - step, py],
                                "pmove": [mx, my],
                            })

        return moves, others

    def is_other_player_piece(self, piece: Piece, other: Optional[Piece] = None) -> bool:
        """Return if the piece is owned by the other player.

        Args:
            piece (`Piece`): The piece to check the player.
            other (`Piece`, optional): Optional piece to reference a player.
        """
        if other:
            return piece.get_player() != other.get_player()
        return piece.get_player() != self.player

    def is_other_player_king(self, piece: Piece, other: Optional[Piece] = None) -> bool:
        """Return if the piece is a king owned by the other player.

        Args:
            piece (`Piece`): The piece to check the player.
            other (`Piece`, optional): Optional piece to reference a player.
        """
        player = other.get_player() if other else self.player
        return isinstance(piece, King) and piece.get_player() != player

    def is_check(self) -> bool:
        """Return if the board's state is 'check'."""
        return self.state == "check"

    def is_unique_move(self, coord: list[int, int], piece: Piece) -> tuple[bool, str]:
        """Return if the pieces move to coord is unique for it's type."""
        px, py = piece.get_coord()

        for other in self.get_player_pieces_like(piece):
            if coord in other.get_options()["moves"]:
                ox, oy = other.get_coord()
                
                overlapp = ""
                if px == ox:
                    overlapp = "row"
                elif py == oy:
                    overlapp = "rank"

                return False, overlapp
        
        return True, ""

    def get_player_pieces(self, player: str, board: list[list[Entity]] = None) -> list[Piece]:
        """Get a player's pieces.

        Args:
            player (str): The player whose pieces shall be returned.
            board (`list` of `list` of `Entity`, optional): list representing a board.

        Returns:
            list: list of the specified player's pieces.
        """
        pieces = []

        if board is None:
            board = self.board

        for row in board:
            for entity in row:
                if isinstance(entity, Piece):
                    if entity.get_player() == player:
                        pieces.append(entity)
        
        return pieces

    def get_player_king(self, player: Optional[str] = None) -> King:
        """Get the player's king."""
        if not player:
            player = self.player

        for piece in self.get_player_pieces(player):
            if isinstance(piece, King):
                return piece

    def get_player_pieces_like(self, piece: Piece, player: Optional[str] = None) -> list[Piece]:
        """Get the player's piece of the same type as the provided piece."""
        if not player:
            player = self.player

        def like(other: Piece):
            return other.__class__ == piece.__class__ and other != piece

        pieces = self.get_player_pieces(player)
        return list(filter(like, pieces))

    def get_player_options(self, player: Optional[str] = None, board: list[list[Entity]] = None,
                           attacking: bool = False, include_piece_coord: bool = False, save: bool = True) -> list[list[int]]:
        """Find all valid moves of a player's pieces.

        Args:
            player (`str`): The player whose pieces shall be returned.
            board (`list` of `list` of `Entity`, optional): list representing a board.
            attacking (`bool`, optional): States if only moves that attack enemy pieces shall be returned.
            include_piece_coord (`bool`, optional): States if a pieces coordinate shall be added to it's moves.

        Returns:
            options: list of all legal moves the player can make.
        """
        options = []

        if player is None:
            player = self.player

        if board is None:
            board = self.board
        
        for piece in self.get_player_pieces(player, board=board):
            moves, others = self.get_piece_options(
                piece, attacking=attacking, board=board)

            if save:
                x, y = piece.get_coord()
                self.board[y][x].set_options({
                    "moves": moves,
                    "others": others
                })

            if include_piece_coord:
                moves.append(piece.get_coord())       

            options += moves

        return options

    def get_other_player_options(self, board: list[list[Entity]] = None, 
                                 include_piece_coord: bool = False, save: bool = True) -> list[list[int]]:
        """Find all squares of the enemy attacks.

        Args:
            board (`list` of `list` of `Entity`, optional): list representing a board.
            with_pieces (`bool`, optional): States if a pieces coordinate shall be added to it's moves.

        Returns:
            list: list of coordinates the enemy attacks.

        Todos:
            TODO: Add valid example.
        """
        if board is None:
            board = self.board

        return self.get_player_options(self.other_player(), board=board, attacking=True, 
                                       include_piece_coord=include_piece_coord, save=save)

    def clear(self) -> None:
        """Cleares the boards entities dynamic attributes."""
        for y in range(8):
            for x in range(8):
                entity = self.board[y][x]

                entity.set_attacked(False)
                if isinstance(entity, Piece):
                    entity.set_options({"moves": [], "others": []})
                    entity.set_pinned(False)
                    entity.set_pinner(None)
                
                self.board[y][x] = entity
    
    def update(self) -> None:
        """Update the board with respect to the new position."""
        self.clear()

        options = self.get_other_player_options()

        for x, y in options:
            self.board[y][x].set_attacked(True)

        # Check if king is in check.
        if self.get_player_king().is_attacked():
            self.state = "check"

        options = self.get_player_options()

        # Update board state.
        if self.state == "check":
            if options:
                self.state = "check"
            else:
                self.state = "checkmate"
        else:
            if not options:
                self.state = "stalemate"
        if self.draw_insufficient_material():
            self.state = "draw"

    def draw_insufficient_material(self) -> bool:
        """Return if neither player can win."""
        return (self.player_insufficient_material("white")
                and self.player_insufficient_material("black"))

    def player_insufficient_material(self, player):
        """Return if the player has insufficient material to win."""
        pieces = self.get_player_pieces(player)

        # With Pawm, Rook or Queen the player has sufficient material.
        if any(isinstance(piece, (Pawn, Rook, Queen)) for piece in pieces):
            return False

        # Check if only king or only king and knight or bishop are on the board.
        if len(pieces) == 1 or len(pieces) == 2:
            return True

        # Check if any the player has knights on the board.
        if any(isinstance(piece, Knight) for piece in pieces):
            return False
        
        bishops = list(filter(lambda piece: isinstance(piece, (Bishop)), pieces))
        colors = [self.get_coord_color(piece.get_coord()) for piece in bishops]
        # Check if all of the bishops are of the same color.
        if all(color == colors[0] for color in colors):
            return True

        return False

    def get_coord_color(self, coord) -> str:
        """Return the color of the square on the board at coord."""
        x, y = coord

        if (x + y) % 2 == 0:
            return "white"
        return "black"

    def next_turn(self) -> None:
        """Set up the next turn."""
        self.player = self.other_player()
        self.update()

    def other_player(self) -> str:
        """Return the other player with respect to the current player."""
        return "white" if self.player == "black" else "black"

    def can_player_castle(self, piece: Piece, 
                          find_others: bool, attacking: bool) -> bool:
        """Return if player can castle.

        Args:
            piece (`Piece`): Selected piece on the chess board.
            find_others (`bool`): States if castling shall be considered.
            attacking (`bool`): States if only attacking moves shall be added.

        Returns:
            bool: Can the player castle?
        """
        return (
            self.state != "check"
            and isinstance(piece, King) 
            and find_others 
            and not attacking
        )

    def to_dict(self) -> dict:
        """Return a JSON representation of the board."""
        pieces = self.get_player_pieces("white") + self.get_player_pieces("black")
        pieces = [piece.to_dict() for piece in pieces]

        return {
            "state": self.state,
            "player": self.player,
            "last": self.last,
            "pieces": pieces
        }

    def from_dict(self, json: dict) -> None:
        """Reconstruct the board from JSON."""
        self.state = json["state"]
        self.player = json["player"]
        self.last = json["last"]

        self.set(empty_board())

        for i in json["pieces"]:
            coord = dict_to_coord(i["coord"])
            piece = str_to_piece(i["type"], coord, i["player"])

            options = i["options"]
            piece.set_options({
                "moves": dict_to_coord(options["moves"], as_list=True),
                "others": options["others"]
            })
            piece.set_pinned(i["pinned"])
            piece.set_pinner(i["pinner"])

            x, y = coord
            self.board[y][x] = piece

        self.update()            

    def view(self, squares: list[list[int]] = []) -> str:
        """View of the current board.

        Args:
            squares (`list` of `list` of `int`): list of squares on the chess board that shall be marked.
        
        Returns:
            str: A string representation of the chess board.
        
        Example:
            >>> board = Board()
            >>> print(board.view())
            ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ 
            ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ ♟︎
            ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
            ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
            ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
            ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
            ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙
            ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖
        """
        board = ""

        for y, row in enumerate(self.board):
            line = ""
            for x, square in enumerate(row):
                if [x, y] in squares:
                    line += "⛝ "
                else:
                    line += str(square) + " "
            board += line + "\n"

        return board

    def show(self, squares: list[list[int]] = []) -> None:
        """Show the current board.
        
        Args:
            squares (`list` of `list` of `int`): list of squares on the chess board that shall be marked.
        """
        print(self.view(squares))


def initial_board() -> list[list[Entity]]:
    """Create a nested list of Entitys that represents the chess board.

    Note:
        The chess board is build with the position 
        'a8' at the coordinate (0, 0) (h1 --> (7, 7)).
        Reminder: Coordinates have to be translated!
        This function is called in the constructor.

    Example:
        >>> from pycheese.core.board import *
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
        Rook([0, 0], "black"), 
        Knight([1, 0], "black"), 
        Bishop([2, 0], "black"), 
        Queen([3, 0], "black"), 
        King([4, 0], "black"), 
        Bishop([5, 0], "black"), 
        Knight([6, 0], "black"), 
        Rook([7, 0], "black"),
    ])
    board.append([Pawn([i, 1], "black") for i in range(8)])

    for i in range(4):
        board.append([Empty([j, i + 2]) for j in range(8)])

    board.append([Pawn([i, 6], "white") for i in range(8)])
    board.append([
        Rook([0, 7], "white"), 
        Knight([1, 7], "white"), 
        Bishop([2, 7], "white"), 
        Queen([3, 7], "white"), 
        King([4, 7], "white"), 
        Bishop([5, 7], "white"), 
        Knight([6, 7], "white"), 
        Rook([7, 7], "white"),
    ])
    
    return board

def empty_board() -> list[list[Entity]]:
    """Create a nested list of Entitys that represents an empty chess board.

    Note:
        The chess board is build with the position 
        'a8' at the coordinate (0, 0) (h1 --> (7, 7)).
        Reminder: Coordinates have to be translated!

    Example:
        >>> board = Board()
        >>> board.board = empty_board()
        >>> board.show()
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
        board.append([Empty([j, i]) for j in range(8)])

    return board


def str_to_piece(type: str, coord: list[int], player: str, whitelist: Optional[set] = None) -> Piece:
    """Return a piece via it's type and other params.

    Args:
        type (str): Name of the class of the `Piece` object. 
        coord (:obj:`list` of :obj:`int`): Coordinate of the piece on board.
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