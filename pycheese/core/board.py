# -*- coding: utf-8 -*-
"""Objec-oriented representation of a chessboard.

This module contains code that represents
a chessboard in an object-oriented style.

Example:
    >>> board = Board()
    >>> print(b.view())
    ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ 
    ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ ♟︎
    ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
    ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
    ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
    ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡ ⊡
    ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙
    ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖
    >>> board.inspect((0, 6))
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
    >>> board.move((0, 6), (0, 5))
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
    >>> print(board.view())
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

from typing import Type
from typing import List
from typing import Tuple
from typing import Union
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

import pycheese.core.utils as utils

from pycheese.core.error import NotInPlayersPossesionException
from pycheese.core.error import NoPieceAtSpecifiedCoordinateException
from pycheese.core.error import MoveNotLegalException

import copy


class Board:
    """Object-oriented representation of a chess board.

    Args:
        json (dict): A JSON representation of an objects this class produces.

    Attributes:
        state (str): State of the game (`ongoing`/`check`/`checkmate`/`stalemate`).
        player (str): String that identifies the player whose turn it is.
        board (`list` of `list` of `Entity`): List representing the board.
    """
    def __init__(self, json: Optional[dict] = None):
        self.state = "ongoing"
        self.player = "white"

        self.board = []
        self.init(json)

    def set(self, board: List[List[Type[Entity]]]) -> None:
        self.board = board

    def get(self) -> List[List[Type[Entity]]]:
        return self.board

    def init(self, json: Optional[dict]) -> None:
        """Initialize the Board classes board.
        
        Args:
            json (dict): A JSON representation of an objects this class produces.
        """
        if json:
            self.from_json(json)
        else:
            self.set(utils.initial_board())
            self.update()

    def move(self, source_coord: Union[str, Tuple[int, int]], 
             target_coord: Union[str, Tuple[int, int]],
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
            source_coord (str or `tuple` of `int`): Initial coordinate of entity on board.
            target_coord (str or `tuple` of `int`): Target coordinate of entity on board.
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
            >>> board.move((0, 6), (0, 5))
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

        boundary = utils.Boundary(0, 8)

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
    
            # TODO: Get piece moves via options.
            # TODO: Figure out way to add companion moves to options.
            source_moves, others = self.get_piece_options(
                source_entity, source_coord)

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
                            self.board[cy][cx] = Empty((cx, cy))

                            # Place the `companion` at the new coordinate.
                            companion.set_coord((x, y))
                            self.board[y][x] = companion

                            # Place the `source_entity` at the new coordinate.
                            source_entity.set_coord((tx, ty))
                            self.board[ty][tx] = source_entity

                            # Place ``Empty`` at the king former coordinate. 
                            self.board[sy][sx] = Empty((sx, sy))

                            side = "queenside" if tx < 4 else "kingside" 
                            event = {"type": "castle", "extra": side}
                            break
                else:
                    if isinstance(source_entity, Pawn) and (ty == 0 or ty == 7):
                        # Request promotion target if is None.
                        if promotion_target is None:
                            event = {"type": "missing_promotion_target", "extra": None}

                        self.board[ty][tx] = utils.str_to_piece(
                            promotion_target, target_coord, self.player, whitelist={"Queen", "Rook", "Bishop", "Knight"})

                        # TODO: Check castle behavoir rook gets chosen. (Note: New rook hasn't moved.)
                        event = {"type": "promotion", "extra": promotion_target}

                    else:
                        if isinstance(self.board[ty][tx], Piece):
                            # TODO: Add hint if piece of same type could also capture.
                            event = {"type": "captures", "extra": None}

                        if (isinstance(source_entity, (Rook, King))):
                            # TODO: Check if works!
                            source_entity.did_move()
                            
                        # TODO: Add hint if piece of same type could move there.
                        # Like: event = {"type": "move", "extra": "unique"/"multiple"}
                        source_entity.set_coord(target_coord)
                        self.board[ty][tx] = source_entity

                    self.board[sy][sx] = Empty((sx, sy))
                
                # Set up for next turn.
                self.next_turn()
        
        return {
            "state": self.state, 
            "source_coord": utils.coord_to_json(source_coord), 
            "target_coord": utils.coord_to_json(target_coord),
            "event": event
        }

    def inspect(self, coord: tuple[int, int]) -> dict:
        """Inspect a piece's moves.

        Get the moves of a current player's piece
        that is identified via it's coordinate on the board.

        Args:
            coord (`tuple` of int): Coordinate on the chess board.

        Returns:
            dict: Dictionary that represents data about a pieces moves.

        Raises:
            ValueError: If the source and target coordinate are equal or out of bounds.
            NotInPlayersPossesionException: The source coordinate isn't under the current players posession.
            NoPieceAtSpecifiedCoordinateException: There is no piece at the coordinate.

        Example:
            >>> board = Board()
            >>> board.inspect((0, 6))
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
        boundary = utils.Boundary(0, 8)
        if not (boundary.accepts((x, y))):
            raise ValueError(f"The piece coordinate is out of bounds: {coord}")

        entity = self.board[y][x]

        if isinstance(entity, Piece):
            if entity.get_player() != self.player:
                raise NotInPlayersPossesionException(
                    "The piece at source coordinate is not in the current player's possesion!")
    
            piece_moves, _ = self.get_piece_options(
                entity, coord, find_others=False)

            return {
                "coord": utils.coord_to_json(coord),
                "piece": entity.to_json(entity),
                "moves": utils.coord_to_json(piece_moves, as_list=True)
            }
        
        raise NoPieceAtSpecifiedCoordinateException(
                "There is no piece at the specified coordinate. {}".format(coord))

    def get_piece_options(self, piece: Type[Piece], board: List[List[Type[Entity]]] = None,
                          find_others: bool = True, attacking: bool = False, ) -> List[Tuple[int, int]]:
        """Find a pieces legal moves.

        Args:
            piece (`Piece`): A piece of the current player.
            piece_coord (`tuple` of `int`): Coordinate of the piece on the chessboard.
            find_other (bool, optional): States if information about companion moves shall be returned.
            attacking (bool, optional): States if only moves that attack enemy pieces shall be returned.
            board (`list` of `list` of `Entity`, optional): List representing a board.

        Returns:
            tuple: piece_moves and companion moves
                * piece_moves (`list` of `list` of int): 
                    List of coordinates that can be legally accessed by the piece.
                * others (`list` of `dict`):
                    List of dicts of data associated with other legal moves (e.g. for castling).
                    The dict inside the list are of shape:
                        {
                            "companion": `Piece`,
                            "others": `list` of `tuple` of `int`
                            "piece_moves": `list` of `tuple` of `int`
                        }

        Example:
            >>> board = Board()
            >>> x, y = (0, 6)
            >>> piece = board.board[y][x]
            >>> board.get_piece_moves(piece, (x, y))
            ([(0, 5), (0, 4)], [])
        """
        moves = []
        others = []

        px, py = piece.get_coord()
        pmoves = piece.get_moves()

        # If no `board` is specified select the position (`self.board`).
        if board is None:
            board = self.board

            # Return the piece's options if they are already known.
            if piece.get_options():
                return piece.get_options()

        boundary = utils.Boundary(0, 8)
        for move in pmoves:
            dx, dy = move

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

                # TODO: PLS Rewrite!!!
                # Check if a `piece` is at the current coordinate.
                square = board[y][x]
                if isinstance(square, Piece):
                    # If the `piece` is owned by the current `player` break.
                    same_player_possesion = square.get_player() == piece.get_player()

                    if attacking:
                        if same_player_possesion:
                            loop = False
                    else:
                        if same_player_possesion:
                            break
                        else:
                            loop = False

                    # The `piece` could take the king. The king is in `check`
                    # and no more moves of the `piece` have to be checked.
                    check = False
                    if isinstance(square, King) and not attacking:
                        self.state = "check"
                        check = True
                        loop = False
    
                    # Check if the `piece` could check the enemy king
                    # if a enemy `piece` would move. Set this `piece` to `pinned`.
                    if not check and isinstance(piece, (Bishop, Rook, Queen)): 
                        tmp_x = x
                        tmp_y = y
                        while boundary.accepts((tmp_x + dx, tmp_y + dy)):
                            tmp_x += dx
                            tmp_y += dy

                            tmp_square = board[tmp_y][tmp_x]
                            if isinstance(tmp_square, Piece):
                                if tmp_square.get_player() != piece.get_player() and isinstance(tmp_square, King):
                                    sx, sy = square.get_coord()
                                    self.board[sx, sy].set_pinned(True)
                                    self.board[sx, sy].set_attacker(piece.get_coord())

                moves.append((x, y))
                
                # End the loop for `pieces` of type ``Pawn``, ``Knight`` or ``King``,
                # because they can only move one square (except ``Pawns``).
                if isinstance(piece, (Pawn, Knight, King)):
                    break

        # Check if the `piece` is of type ``Pawn``
        # and can execute it's unique movement.
        if isinstance(piece, Pawn):
            attacking_moves = []

            pmoves = piece.get_attack_moves()
            for move in pmoves:
                dx, dy = move

                # Invert the movement for white `pieces`, 
                # because of the way the board has ben initialized.
                if piece.get_player() == "white":
                    dy *= -1

                x, y = px + dx, py + dy

                if boundary.accepts((x, y)):
                    # Check if a `piece` is at the current coordinate.
                    square = board[y][x]

                    # Add the coordinate to `attacking_moves` if
                    # a ``Piece`` of the enemy is at the coordinate.
                    if (not attacking and isinstance(square, Piece)):
                        if square.get_player() != piece.get_player():
                            attacking_moves.append((x, y))
                    # Add the coordinate to `attacking_moves` regardless
                    # of the fact that a ``Piece`` is at the coordinate.
                    # Because all attacking moves are recoorded.
                    # Check only if a chess piece is in the opponent's possession.
                    elif attacking:
                        if isinstance(square, Piece):
                            if square.get_player() != piece.get_player():
                                attacking_moves.append((x, y))
                        else:
                            attacking_moves.append((x, y))    

            # If only attacking moves shall be recoorded,
            # `piece_moves` equal `attacking_moves`.
            if attacking:
                moves = attacking_moves

            # Else append the `attacking_moves` to `piece_moves`
            # and check if the ``Pawn`` can execute it's special move.
            else:
                for move in attacking_moves:
                    moves.append(move)

                if piece.can_special():
                    dx, dy = piece.get_special_move()

                    if piece.get_player() == "white":
                        dy *= -1

                    x, y = px + dx, py + dy
                    
                    if isinstance(board[y][x], Empty):
                        moves.append((x, y))
        
        # Check if `piece` is `pinned`. If the `piece` is `pinned`
        # it can only move in the `attackers` direction.
        # To compute the legal moves keep the coordinates
        # in the `attackers` `line_of_attack`
        # (the attackers moves towards the king).
        if piece.is_pinned():
            ax, ay = piece.get_attacker()
            attacker = board[ay][ax]

            dx, dy = ax - px, ay - py
            dx, dy = utils.normalize(dx), utils.normalize(dy)

            start_x, stop_x = min(ax, px), max(ax, px)
            xboundary = utils.Boundary(start_x, stop_x)
            
            start_y, stop_y = min(ay, py), max(ay, py)
            yboundary = utils.Boundary(start_y, stop_y)

            x, y = px, py
            tmp_moves = []
            while xboundary.accepts(x + dx) and yboundary.accepts(y + dy):
                x += dx
                y += dy

                tmp_moves.append((x, y))

            moves = list(filter(lambda move: move in tmp_moves, moves))

        # If the `player` is in check: Find all moves that resolve the check.
        # Therefore check if the piece is in the checked players possesion.
        if self.state == "check" and piece.get_player() == self.player:
            # If the `piece` is of type ``King`` then only moves
            # that lead to non attacked coordinates are valid.
            if isinstance(piece, King):
                tmp_moves = []
                
                for move in moves:
                    x, y = move
                    if not board[y][x].is_attacked():
                        tmp_moves.append(move)
                
                moves = tmp_moves
            # Else find the king and all moves of the
            # `piece` that hide the king from check.
            else:
                king = self.get_player_king()

                # List of all moves to avoid check.
                tmp_moves = []

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
                        x, y = move

                        tmp_board[y][x] = piece
                        tmp_board[py][px] = Empty((px, py))

                        if king.get_coord() not in self.get_other_player_options(board=tmp_board):
                            tmp_moves.append(move)

                self.state = "check"
                moves = tmp_moves

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
                            square = board[py][x]

                            if isinstance(square, Piece) or square.is_attacked():
                                path_not_obstructed = False
                                break

                        if path_not_obstructed:
                            mx, my = px + step * 2, py
                            moves.append((mx, my))
                            
                            # TODO: Update comments that reference companion as `Piece`.
                            others.append({
                                "companion": companion.get_coord(),
                                "cmove": (mx - step, py),
                                "pmove": (mx, my),
                            })

        return moves, others

    def get_player_pieces(self, player: str, board: List[List[Type[Entity]]] = None) -> List[Type[Piece]]:
        """Get a player's pieces.

        Args:
            player (str): The player whose pieces shall be returned.
            board (`list` of `list` of `Entity`, optional): List representing a board.

        Returns:
            list: List of the specified player's pieces.

        Example:
            >>> board = Board()
            >>> pieces = board.get_player_pieces("white")
            >>> [piece.to_json() for piece in pieces]
            [
                {'type': 'Pawn', 'player': 'white', 'coord': {'x': 0, 'y': 6}, 'pinned': False, 'attacker': None}, 
                ...
                {'type': 'Pawn', 'player': 'white', 'coord': {'x': 7, 'y': 6}, 'pinned': False, 'attacker': None},
                {'type': 'Rook', 'player': 'white', 'coord': {'x': 0, 'y': 7}, 'pinned': False, 'attacker': None}, 
                {'type': 'Knight', 'player': 'white', 'coord': {'x': 1, 'y': 7}, 'pinned': False, 'attacker': None}, 
                {'type': 'Bishop', 'player': 'white', 'coord': {'x': 2, 'y': 7}, 'pinned': False, 'attacker': None}, 
                {'type': 'Queen', 'player': 'white', 'coord': {'x': 3, 'y': 7}, 'pinned': False, 'attacker': None}, 
                {'type': 'King', 'player': 'white', 'coord': {'x': 4, 'y': 7}, 'pinned': False, 'attacker': None}, 
                {'type': 'Bishop', 'player': 'white', 'coord': {'x': 5, 'y': 7}, 'pinned': False, 'attacker': None}, 
                {'type': 'Knight', 'player': 'white', 'coord': {'x': 6, 'y': 7}, 'pinned': False, 'attacker': None}, 
                {'type': 'Rook', 'player': 'white', 'coord': {'x': 7, 'y': 7}, 'pinned': False, 'attacker': None}
            ]

            TODO: Upate docstring example.
        """
        pieces = []

        if board is None:
            board = self.board

        for row in board:
            for square in row:
                if isinstance(square, Piece):
                    if square.get_player() == player:
                        pieces.append(square)
        
        return pieces

    def get_player_king(self, player: Optional[str] = None) -> Type[King]:
        """Get the player's king."""
        if not player:
            player = self.player

        for piece in self.get_player_pieces(player):
            if isinstance(piece, King):
                return piece

    def get_player_options(self, player: str, board: List[List[Type[Entity]]] = None, attacking: bool = False, 
                           include_piece_coord: bool = False, save_options: bool = True) -> List[Tuple[int]]:
        """Find all valid moves of a player's pieces.

        Args:
            player (str): The player whose pieces shall be returned.
            board (`list` of `list` of `Entity`, optional): List representing a board.
            attacking (bool, optional): States if only moves that attack enemy pieces shall be returned.
            include_piece_coord (bool, optional): States if a pieces coordinate shall be added to it's moves.
            save_options (bool, optional): States if a pieces options shall be saved.

        Returns:
            options: List of all legal moves the player can make.
        """
        options = []

        if board is None:
            board = self.board
        
        for piece in self.get_player_pieces(player, board=board):
            moves, other = self.get_piece_options(
                piece, piece.get_coord(), attacking=attacking, board=board)

            if save_options:
                x, y = piece.get_coord()
                self.board[y][x].set_options({
                    "moves": moves,
                    "other": other
                })     

            if include_piece_coord:
                moves.append(piece.get_coord())       

            options += moves

        return options

    def get_other_player_options(self, board: Optional[List[List[Type[Entity]]]] = None, 
                                 include_piece_coord: bool = False) -> List[Tuple[int]]:
        """Find all squares of the enemy attacks.

        Args:
            board (`list` of `list` of `Entity`, optional): List representing a board.
            with_pieces (bool, optional): States if a pieces coordinate shall be added to it's moves.

        Returns:
            list: List of coordinates the enemy attacks.

        Example:
            >>> board = Board()
            >>> board.get_attacked_squares()
            [
                (0, 2), (2, 2), (5, 2), (7, 2), (1, 2), (0, 2), (2, 2), (1, 2), (3, 2), 
                (2, 2), (4, 2), (3, 2), (5, 2), (4, 2), (6, 2), (5, 2), (7, 2), (6, 2)
            ]
        """
        # TODO: Return other player pieces options if board is None.
        # TODO: Else compute the attacked squares of the board.
        if board is None:
            board = self.board

        return self.get_player_options(self.other_player(), board=board, attacking=True, 
                                       include_piece_coord=include_piece_coord)

    def clear(self) -> None:
        """Cleares the boards entities dynamic attributes."""
        for y in range(8):
            for x in range(8):
                entity = self.board[y][x]

                entity.set_attacked(False)
                if isinstance(entity, Piece):
                    entity.set_options(None)
                    entity.set_pinned(False)
                    entity.set_attacker(None)
                
                self.board[y][x] = entity
    
    def update(self) -> None:
        self.clear()
        """Update the board with respect to the new position."""
        # TODO: Update attacker options.
        # TODO: Move update attacked squares components here.
        oplayer_options = self.get_player_options(self.other_player(), attacking=True)
        oplayer_moves, oplayer_other =  oplayer_options

        for x, y in oplayer_moves:
            self.board[y][x].set_attacked(True)

        # Check if king is in check.
        if self.get_player_king().is_attacked():
            self.state = "check"

        # TODO: Update current player options.
        cplayer_options = self.get_player_options(self.player)
        cplayer_moves, cplayer_other =  cplayer_options

        # Update board state.
        if self.state == "check":
            if cplayer_moves:
                self.state = "check"
            else:
                self.state = "checkmate"
        else:
            if not cplayer_moves:
                self.state = "stalemate"

    def next_turn(self) -> None:
        """Set up the next turn."""
        self.player = self.other_player()
        self.update()

    def other_player(self) -> str:
        """Return the other player with respect to the current player."""
        return "white" if self.player == "black" else "black"

    def can_player_castle(self, piece: Type[Piece], 
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

    def to_json(self) -> dict:
        """Return a JSON representation of the board."""
        pieces = self.get_player_pieces("white") + self.get_player_pieces("black")
        pieces = [piece.to_json() for piece in pieces]


        return {
            "state": self.state,
            "player": self.player,
            "pieces": pieces
        }

    def from_json(self, json: dict) -> None:
        """Reconstruct the board from JSON."""
        self.state = json["state"]
        self.player = json["player"]

        self.set(utils.empty_board())

        for i in json["pieces"]:
            coord = utils.json_to_coord(i["coord"])
            player = i["player"]
            
            piece = utils.str_to_piece(i["type"], coord, player)

            piece.set_pinned(i["pinned"])
            piece.set_attacker(i["attacker"])

            # TODO: Add piece options.
            x, y = coord
            self.board[y][x] = piece

        # TODO: Set attacked squares via all piece's options.
        self.update()            

    def view(self, squares: List[Tuple[int]] = []) -> str:
        """View of the current board.

        Args:
            squares (`list` of `tuple` of `int`): List of squares on the chess board that shall be marked.
        
        Returns:
            str: A string representation of the chess board.
        
        Example:
            >>> board = Board()
            >>> print(b.view())
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
                if (x, y) in squares:
                    line += "⛝ "
                else:
                    line += str(square) + " "
            board += line + "\n"

        return board

    def show(self, squares: List[Tuple[int]] = []) -> None:
        """Show the current board.
        
        Args:
            squares (`list` of `tuple` of `int`): List of squares on the chess board that shall be marked.
        """
        print(self.view(squares))

    