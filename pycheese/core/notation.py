# -*- coding: utf-8 -*-
"""Utils to create chess notation for chess games."""


from sys import prefix
from typing import List

from pycheese.core.entity import Piece
from pycheese.core.utils import dict_to_coord


class NotationParser:
    def __init__(self, notation: List[str] = []):
        self.notation = notation

    def add(self, output: dict, piece: Piece):
        pass

    def player(self):
        if self.notation[-1]["white"]:
            return "black"
        return "white"

    def __str__(self):
        notation = []

        for i, turn in enumerate(self.notation):
            notation.extend([f"{i + 1}.", turn["white"], turn["black"]])
        
        return  " ".join(filter(None, notation))

    def switch_eval(self, state, player):
        switch = {"checkmate": "1–0" if player == "white" else "0–1", "draw": "½–½"}
        return switch.get(state)


class AlgebraicNotationParser(NotationParser):
    def __init__(self, notation: List[str] = []):
        super().__init__(notation)

    def add(self, output: dict, piece: Piece):
        state = output["state"]
        event = output["event"]
        scoord, tcoord = dict_to_coord([
            output["source_coord"], 
            output["target_coord"]])

        player = self.player()
        notation = []

        move = ""
        if event["type"] == "castle":
            move = self.switch_castle(event["extra"])
        else:
            move = self.switch_piece(piece) + self.coord(scoord, tcoord, event)

        notation.append(move)
        notation.append(self.switch_state(state, player))
        notation.append(self.switch_eval(player))

        notation = " ".join(filter(None, notation))
        self.notation[-1][player] = notation

        if player == "black":
            notation.append({"white": "", "black": ""})

    def coord(self, scoord, tcoord, event):
        tx, ty = tcoord
        notation = self.switch_rows(tx) + ty
        
        if "multiple" in event.get("extra") :
            sx, sy = scoord

            if "rank" in event.get("extra"):
                notation = sy + notation
            else:
                notation = self.switch_rows(tx) + notation

        return notation

    def switch_rows(self, x):
        return ["a", "b", "c", "d", "e", "f", "g", "h"][x]
        
    def switch_piece(self, piece):
        switch = {"Pawn": "", "Knight": "N", "Bishop": "B", "Rook": "R", "Queen": "Q", "King": "K"}
        return switch.get(piece.__class__)

    def switch_state(self, state):
        switch = {"check": "+", "checkmate": "#"}
        return switch.get(state)

    def switch_castle(self, extra):
        switch = {"kingside": "0-0", "queenside": "0-0-0"}
        return switch.get(extra)


class FigurineAlgebraicNotationParser(AlgebraicNotationParser):
    def __init__(self, notation: List[str] = []):
        super().__init__(notation)

    def switch_piece(self, piece):
        if piece.__class__ == "Pawn":
            return ""
        return str(piece)
    