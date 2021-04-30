# -*- coding: utf-8 -*-
"""Objec-oriented representation of a chessboard.

This module contains code that represents
a chessboard in an object-oriented style.

Example:
    >>> board = Board()
    >>> board("e2")
    >>> board("e2", "e4")
"""


from __future__ import annotations

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

from pycheese.core.utils import Boundary

from pycheese.core.error import NotInPlayersPossesionException

import copy


class Board:
    """Object-oriented representation of a chess board.

    Attributes:
        state (str): State of the game (`ongoing`/`check`/`checkmate`/`stalemate`).
        player (str): String that identifies the player whose turn it is.
        board (:obj:`list` of :obj:`list` of :obj:`Entity`): List representing the board.
    """
    def __init__(self):
        self.state = "ongoing"
        self.player = "white"

        self.board = self.initial_board()
        self.update_attacked_squares()

    def initial_board(self) -> List[List[Type[Entity]]]:
        """Create a nested list of Entitys that represents the chessboard.

        Note:
            The chess board is build with the position 
            'a8' at the coordinate (0, 0) (h1 --> (7, 7)).
            Reminder: Coordinates have to be translated!

        Example:
            >>> board = Board()
            >>> assert board.board = board.initial_board()

        Returns:
            list: Nested list of Entitys that represents the chessboard.
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

    def __call__(self, source_coord: Union[str, Tuple[int, int]], 
                 target_coord: Union[str, Tuple[int, int], None] = None, 
                 promotion_target: Union[str, None] = None):
        """Chessboard interface.

        This function servers as an interface to the chessboard.
        To do so different behaviors are invoked with different inputs.

        The minimal input is the `source_coord`, a coordinate on the board wich
        shall be focused to check for legal moves of the current player. 

        The `target_coord` parameter must be specified additionally
        to move a piece to a desired coordinate - the target coordinate.
        The code checks if `target_coord` is in the legal moves the player
        can make with the piece identified via `source_coord`. If this holds
        true the move will be executed and the next players turn will be
        initiated.

        If a pawn shall be promoted the `promotion_target` parameter must be specified.
        This parameter identifies the type of piece that shall be spawned at the
        `target_coord` coordinate on the chessboard. The pawn at the `source_coord`
        coordinate will be substituted with an entity of type `Empty`.

        Args:
            source_coord (str or :obj:`tuple` of :obj:`int`): Initial coordinate of entity on board.
            target_coord (str or :obj:`tuple` of :obj:`int`, optional): Target coordinate of entity on board.
            promotion_target (str, optional): String that identifies piece to promote pawn into.

        Returns:
            # TODO: RETURN DICT AS OUTPUT
            str: The boards state.

        Example:
            >>> board = Board()
            >>> board("e2")
            >>> board("e2", "e4")
        """
        status = None

        if type(source_coord) is str:
            source_coord = self.translate_coord(source_coord)

        if target_coord is None:
            target_coord = source_coord

        if type(target_coord) is str:
            target_coord = self.translate_coord(target_coord)

        source_x, source_y = source_coord
        target_x, target_y = target_coord
        
        source_entity = self.board[source_y][source_x]
        target_entity = self.board[target_y][target_x]

        if isinstance(source_entity, Piece):

            if source_entity.get_player() != self.player:
                raise NotInPlayersPossesionException(
                    "The specified piece is not in the current player's possesion!")
    
            source_moves, others = self.get_piece_moves(
                source_entity, source_coord)

            if target_coord in source_moves:
                player_moves = self.get_player_moves()
                if self.state == "check":
                    if player_moves:
                        self.state = "ongoing"
                    else:
                        self.state = "checkmate"
                        return {
                            "state": self.state, 
                            "source_coord": source_coord, 
                            "target_coord": target_coord,
                            "status": status,
                        }
            
                else:
                    if not player_moves:
                        self.state = "stalemate"
                        return {
                            "state": self.state, 
                            "source_coord": source_coord, 
                            "target_coord": target_coord,
                            "status": status,
                        }
            
                if others:
                    # Find the companion in the
                    for element in others:
                        companion = element["companion"]
                        companion_move = element["companion_move"]
                        piece_move = element["piece_move"]

                        if target_coord == piece_move:
                            companion_x, companion_y = companion.get_coord()
                            companion.set_coord((x, y))

                            self.board[y][x] = companion
                            self.board[companion_y][companion_x] = Empty((companion_x, companion_y))

                            x, y = (x - 1, y) if (x - 1, y) in source_moves else (x + 1, y)
                            source_entity.set_coord((x, y))

                            self.board[y][x] = source_entity
                            self.board[source_y][source_x] = Empty((source_x, source_y))

                            status = "castling"
                            break
                else:
                    if (isinstance(source_entity, Pawn) and
                        (target_y == 0 or target_y == 7)):
                        # Request promotion target if is None.
                        if promotion_target is None:
                            status = "missing_promotion_target"
                            return {
                                "state": self.state, 
                                "source_coord": source_coord, 
                                "target_coord": target_coord,
                                "status": status,  
                            }

                        self.board[target_y][target_x] = self.get_promotion_target(
                            promotion_target, target_coord)

                        status = "promotion"

                    else:
                        if isinstance(self.board[target_y][target_x], Piece):
                            status = "captures"
                            
                        source_entity.set_coord(target_coord)
                        self.board[target_y][target_x] = source_entity

                    self.board[source_y][source_x] = Empty((source_x, source_y))
                
                if (isinstance(source_entity, Rook) or
                    isinstance(source_entity, King)):
                    source_entity.did_move()

                self.next_turn()
                self.update_attacked_squares()

            if target_entity == source_entity:
                print("Source:", str(source_entity))
                print("Source moves:", source_moves)
            else:
                print("Source:", str(source_entity), "  Target:", str(target_entity))
                print("Source moves:", source_moves, "\nCompanion moves:", others, "\n")

            if target_coord == source_coord:
                self.print(squares=source_moves)
            else:
                self.print()
        
        return {
            "state": self.state, 
            "source_coord": source_coord, 
            "target_coord": target_coord,
            "status": status,  
        }

    def get_piece_moves(self, piece: Type[Piece], piece_coord: Tuple[int, int],
                        attacking: bool = False, board: List[List[Type[Entity]]] = None) -> List[Tupe[int, int]]:
        """Find a pieces legal moves.

        Args:
            piece (:obj:`Piece`): A piece of the current player.
            piece_coord (:obj:`tuple` of :obj:`int`): Coordinate of the piece on the chessboard.
            attacking (bool, optional): States if only moves that attack enemy pieces shall be returned.
            board (:obj:`list` of :obj:`list` of :obj:`Entity`, optional): List representing a board.

        Returns:
            tuple: piece_moves and companion moves
                * piece_moves (:obj:`list` of :obj:`list` of int): 
                    List of coordinates that can be legally accessed by the piece.
                * others (:obj:`list` of :obj:`dict`):
                    List of dicts of data associated with other legal moves (e.g. for castling).
                    The dict inside the list are of shape:
                        {
                            "companion": :obj:`Piece`,
                            "others": :obj:`list` of :obj:`tuple` of :obj:`int`
                            "piece_moves": :obj:`list` of :obj:`tuple` of :obj:`int`
                        }

        Example:
            >>> board = Board()
            >>> coord = (0, 0)
            >>> board.get_piece_moves(board.board[coord[1], coord[0]], coord)
        """
        piece_moves = []
        others = []

        # If no `board` is specified select the position (`self.board`).
        if board is None:
            board = self.board

        piece_x, piece_y = piece_coord
        moves = piece.get_moves()

        boundary = Boundary(0, 8)
        for move in moves:
            dx, dy = move

            # Invert the movement for white `pieces`, 
            # because of the way the board has ben initialized.
            if piece.get_player() == "white":
                dy = - dy

            # Traverse the path given by the movement of the `piece` types
            # from the `piece` coordinate and recoord the coordinates
            # until another `piece` was found or the coordinate is out of bounds.
            # These recoorded coordinates are regarded as the legal moves.
            
            x = piece_x
            y = piece_y

            loop = True
            while loop and boundary.accepts(x + dx) and boundary.accepts(y + dy):
                x += dx
                y += dy

                # Check if a `piece` is at the current coordinate.
                square = board[y][x]
                if isinstance(square, Piece):
                    # If the `piece` is owned by the current `player` break.
                    if (isinstance(piece, Pawn) or
                        square.get_player() == piece.get_player()):
                        break

                    # If the `piece` is owned by the enemy `player`
                    # add the coordinate to the list of legal moves.
                    if square.get_player() != piece.get_player():
                        loop = False

                    # The `piece` could take the king. The king is in `check`
                    # and no more moves of the `piece` have to be checked.
                    check = False
                    if isinstance(square, King):
                        self.state = "check"
                        check = True
                        loop = False
    
                    # Check if the `piece` could check the enemy king
                    # if a enemy `piece` would move. Set this `piece` to `pinned`.
                    if (not check and
                        (isinstance(piece, Bishop) or
                         isinstance(piece, Rook) or
                         isinstance(piece, Queen))): 
                        tmp_x = x
                        tmp_y = y
                        while boundary.accepts(tmp_x + dx) and boundary.accepts(tmp_y + dy):
                            tmp_x += dx
                            tmp_y += dy

                            tmp_square = board[tmp_y][tmp_x]
                            if isinstance(tmp_square, Piece):
                                if tmp_square.get_player() == piece.get_player():
                                    break
                                else:    
                                    if isinstance(tmp_square, King):
                                        square.set_pinned(True, attacker=piece)
                                    else:
                                        break 

                piece_moves.append((x, y))
                
                # End the loop for `pieces` of type ``Pawn``, ``Knight`` or ``King``,
                # because they can only move one square (except ``Pawns``).
                if (isinstance(piece, Pawn) or
                    isinstance(piece, Knight) or
                    isinstance(piece, King)):
                    break

        # Check if the `piece` is of type ``Pawn``
        # and can execute it's unique movement.
        if isinstance(piece, Pawn):
            attacking_moves = []

            moves = piece.get_attack_moves()
            for move in moves:
                dx, dy = move

                # Invert the movement for white `pieces`, 
                # because of the way the board has ben initialized.
                if piece.get_player() == "white":
                    dy = - dy

                x = piece_x + dx
                y = piece_y + dy

                if boundary.accepts(x) and boundary.accepts(y):
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
                piece_moves = attacking_moves
            # Else append the `attacking_moves` to `piece_moves`
            # and check if the ``Pawn`` can execute it's special move.
            else:
                for move in attacking_moves:
                    piece_moves.append(move)

                if piece.can_special():
                    dx, dy = piece.get_special_move()
                    if piece.get_player() == "white":
                        dy = - dy

                    piece_moves.append((piece_x + dx, piece_y + dy))
        
        # Check if `piece` is `pinned`. If the `piece` is `pinned`
        # it can only move in the `attackers` direction.
        # To compute the legal moves keep the coordinates
        # in the `attackers` `line_of_attack`
        # (the attackers moves towards the king).
        if piece.is_pinned():
            attacker = piece.get_attacker()

            attacker_x, attacker_y = attacker.get_coord()
            dx = attacker_x - piece_x
            dy = attacker_y - piece_y

            def normalize(x: int) -> int:
                """Normalize an integer between -1 and 1."""
                if x > 0:
                    return 1
                elif x < 0:
                     return -1
                return 0

            dx = normalize(dx)
            dy = normalize(dy)

            line_of_attack = []

            start_x = min(attacker_x, piece_x)
            stop_x = max(attacker_x, piece_x)
            boundary_x = Boundary(start_x, stop_x)
            
            start_y = min(attacker_y, piece_y)
            stop_y = max(attacker_y, piece_y)
            boundary_y = Boundary(start_y, stop_y)

            x = piece_x
            y = piece_y
            while boundary_x.accepts(x + dx) and boundary_y.accepts(y + dy):
                x += dx
                y += dy

                line_of_attack.append((x, y))

            tmp_piece_moves = []
            for move in piece_moves:
                if move in line_of_attack:
                    tmp_piece_moves.append(move)

            piece_moves = tmp_piece_moves

        # If the `player` is in check: Find all moves that resolve the check.
        # Therefore check if the piece is in the checked players possesion.
        if (self.state == "check"
            and piece.get_player() == self.player
            and isinstance(piece, Piece)):

            # If the `piece` is of type ``King`` then only moves
            # that lead to non attacked coordinates are valid.
            if isinstance(piece, King):
                tmp_piece_moves = []
                
                for move in piece_moves:
                    x, y = move
                    if not board[y][x].is_attacked():
                        tmp_piece_moves.append(move)
                
                piece_moves = tmp_piece_moves
            # Else find the king and all moves of the
            # `piece` that hide the king from check.
            else:
                king = None

                for piece in self.get_player_pieces(self.player):
                    if isinstance(piece, King):
                        king = piece
                        break
                
                king_coord = king.get_coord()

                # List of all moves to avoid check.
                tmp_piece_moves = []

                # Set the `state` temporary to "ongoing" to look
                # into future positions without restrictions.
                self.state = "ongoing"

                # To block check the `piece` has to step into
                # squares on the board that are being attacked by the enemy.
                # Compute theese and check if the king is hidden from check.
                attacked_squares = self.get_attacked_squares(with_attackers=True)

                for move in piece_moves:
                    if move in attacked_squares:
                        tmp_board = copy.deepcopy(board)
                        x, y = move

                        tmp_board[y][x] = piece
                        tmp_board[piece_y][piece_x] = Empty((piece_x, piece_y))

                        tmp_attacked_squares = self.get_attacked_squares(board=tmp_board)

                        if king_coord not in tmp_attacked_squares:
                            tmp_piece_moves.append(move)

                self.state = "check"
                piece_moves = tmp_piece_moves

        # Check if the player can castle.
        # To so first check if the king has already moved or a given rook
        # who is identified by the side the `target_coord` leads to.
        # Afterwards check if the enemy is attacking squares that
        # are needed for castling or if theese squares are .
        if (self.state != "check"
            and not attacking
            and isinstance(piece, King)):
            # Check if king has already moved.
            if not piece.get_moved():
                for step in range(-1, 2, 2):
                    companion_x = 0 if step == -1 else 7
                    companion_y = piece_y
                    companion = board[companion_y][companion_x]
                    # Check if the `companion` of type `Rook` has already moved.
                    if (isinstance(companion, Rook)
                        and not companion.get_moved()):

                        # Check for obstructed or attacked squares. 
                        empty = True

                        start = 5 if step == 1 else 1
                        stop = 7 if step == 1 else 4

                        for x in range(start, stop):
                            square = board[piece_y][x]
                            if isinstance(square, Piece) or square.is_attacked():
                                empty = False
                                break

                        if empty:
                            piece_move = (piece_x + step * 2, piece_y)
                            piece_moves.append(piece_move)
                            
                            companion_move = (piece_x + -step, piece_y)
                            others.append({
                                "companion": companion,
                                "companion_move": companion_move,
                                "piece_move": piece_move,
                            })

        return piece_moves, others

    def get_player_pieces(self, player: str, 
                          board: List[List[Type[Entity]]] = None) -> List[Type[Piece]]:
        """Get a player's pieces.

        Args:
            player (str): The player whose pieces shall be returned.
            board (:obj:`list` of :obj:`list` of :obj:`Entity`, optional): List representing a board.

        Returns:
            list: List of the specified player's pieces.

        Example:
            >>> board = Board()
            >>> board.get_player_pieces("white")
        """
        player_pieces = []

        if board is None:
            board = self.board

        for row in board:
            for square in row:
                if isinstance(square, Piece):
                    if square.get_player() == player:
                        player_pieces.append(square)
        
        return player_pieces

    def get_player_moves(self, player: str, board: List[List[Type[Entity]]] = None, 
                         attacking: bool = False, with_pieces: bool = False) -> List[Tuple[int]]:
        """Find all valid moves of a player's pieces.

        Args:
            player (str): The player whose pieces shall be returned.
            board (:obj:`list` of :obj:`list` of :obj:`Entity`, optional): List representing a board.
            attacking (bool, optional): States if only moves that attack enemy pieces shall be returned.
            with_pieces (bool, optional): States if a pieces coordinate shall be added to it's moves.

        Returns:
            moves: List of all legal moves the player can make.

        Example:
            >>> board = Board()
            >>> board.get_player_moves("white")
        """
        moves = []

        if board is None:
            board = self.board
                            
        pieces = self.get_player_pieces(player, board=board)
        
        for piece in pieces:
            piece_moves = self.get_piece_moves(
                piece, piece.get_coord(), board=board, attacking=attacking)

            for move in piece_moves[0]:
                moves.append(move)
        
            if with_pieces:
                moves.append(piece.get_coord())
        
        return moves

    def get_attacked_squares(self, board: List[List[Type[Entity]]] = None, 
                             with_pieces: bool = False) -> List[Tuple[int]]:
        """Find all squares of the enemy attacks.

        Args:
            board (:obj:`list` of :obj:`list` of :obj:`Entity`, optional): List representing a board.
            with_pieces (bool, optional): States if a pieces coordinate shall be added to it's moves.

        Returns:
            list: List of coordinates the enemy attacks.

        Example:
            >>> board = Board()
            >>> board.get_attacked_squares()
        """
        if board is None:
            board = self.board

        player = "white" if self.player == "black" else "black"

        attacked_squares = self.get_player_moves(
            player,
            board=board,
            attacking=True, 
            with_pieces=with_pieces,
        )

        return attacked_squares
    
    def update_attacked_squares(self) -> None:
        """Update the pieces `attacked` and `pinned` attributes.
        
        This function should be called after the `self.next_turn()` function
        to update the chessboard and account for the new position.

        Note:
            This function is called automatically.

        Example:
            >>> board = Board()
            >>> board("e2", "e4")
            >>> board.update_attacked_squares()
        """
        for row in self.board:
            for square in row:
                if isinstance(square, Piece) and square.is_pinned():
                    square.set_attacked(False)
                    square.set_pinned(False)
                    square.set_attacker(None)

        attacked_squares = self.get_attacked_squares()
        for square in attacked_squares:
            x, y = square
            self.board[y][x].set_attacked(True)
    
    def get_promotion_target(self, promotion_target: str, 
                             target_coord: Tuple[int]) -> Type[Piece]:
        """Get the piece that is requested when a pawn reaches the enemy's baseline.

        Note:
            The promotion target can either be: queen/rook/bishop/knight

        Args:
            promotion_target (str, optional): String that identifies piece to promote pawn into.
            target_coord (str or :obj:`tuple` of :obj:`int`, optional): Target coordinate of entity on board.    
        """
        if promotion_target == "queen":
            return Queen(target_coord, self.player)
        elif promotion_target == "rook":
            return Rook(target_coord, self.player)
        elif promotion_target == "bishop":
            return Bishop(target_coord, self.player)
        elif promotion_target == "knight":
            return Knight(target_coord, self.player)

    def next_turn(self) -> None:
        """Change the player the indicate the next turn."""
        self.player = "white" if self.player == "black" else "black"
    
    def translate_coord(self, coord: str) -> Tuple[int]:
        """Translate a coordinate in chess notation into the internal representation.
        
        Examples: 'a1' --> (0, 7); 'h8' --> (7, 0)

        Args:
            coord -- coordinate in chess notation (lowercase letter [a-h] followed by integer [1-8])

        Returns:
            tuple -- translated (x, y) coordinate
        """
        x = coord[0]
        y = coord[1]

        x = ord(x) - ord("a")
        y = abs(int(y) - 8)

        return x, y

    def print(self, squares=None, show_attacked=False) -> None:
        """Print the current board.

        Args:
            squares -- list of squares on the chess board that shall be marked with this character '⛝' (to indicate that they are attacked)
            show_attacked -- boolean that states if all attacked squares shall be marked
        """

        if squares is None:
            squares = []

        attacked = []
        if show_attacked:
            for y, row in enumerate(self.board):
                for x, square in enumerate(row):
                    if square.is_attacked():
                        attacked.append((x, y))

        for y, row in enumerate(self.board):
            line = []
            for x, square in enumerate(row):
                if (x, y) in squares:
                    line.append("⛝")
                elif (x, y) in attacked:
                    line.append("%")
                else:
                    line.append(str(square))
            print(line)
        print()

