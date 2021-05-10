# -*- coding: utf-8 -*-
"""Unittests for code in the board module.

This module contains code to test the content
of the pycheese.core.board module using pytest.
"""


def case_initial_board() -> dict:
    return {
        'state': 'ongoing', 
        'player': 'white', 
        'pieces': [
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 0, 'y': 6}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 1, 'y': 6}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 2, 'y': 6}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 3, 'y': 6}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 4, 'y': 6}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 5, 'y': 6}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 6, 'y': 6}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 7, 'y': 6}, 'pinned': False, 'attacker': None}, 
            {'type': 'Rook', 'player': 'white', 'coord': {'x': 0, 'y': 7}, 'pinned': False, 'attacker': None}, 
            {'type': 'Knight', 'player': 'white', 'coord': {'x': 1, 'y': 7}, 'pinned': False, 'attacker': None}, 
            {'type': 'Bishop', 'player': 'white', 'coord': {'x': 2, 'y': 7}, 'pinned': False, 'attacker': None}, 
            {'type': 'Queen', 'player': 'white', 'coord': {'x': 3, 'y': 7}, 'pinned': False, 'attacker': None}, 
            {'type': 'King', 'player': 'white', 'coord': {'x': 4, 'y': 7}, 'pinned': False, 'attacker': None}, 
            {'type': 'Bishop', 'player': 'white', 'coord': {'x': 5, 'y': 7}, 'pinned': False, 'attacker': None}, 
            {'type': 'Knight', 'player': 'white', 'coord': {'x': 6, 'y': 7}, 'pinned': False, 'attacker': None}, 
            {'type': 'Rook', 'player': 'white', 'coord': {'x': 7, 'y': 7}, 'pinned': False, 'attacker': None}, 
            {'type': 'Rook', 'player': 'black', 'coord': {'x': 0, 'y': 0}, 'pinned': False, 'attacker': None}, 
            {'type': 'Knight', 'player': 'black', 'coord': {'x': 1, 'y': 0}, 'pinned': False, 'attacker': None}, 
            {'type': 'Bishop', 'player': 'black', 'coord': {'x': 2, 'y': 0}, 'pinned': False, 'attacker': None}, 
            {'type': 'Queen', 'player': 'black', 'coord': {'x': 3, 'y': 0}, 'pinned': False, 'attacker': None}, 
            {'type': 'King', 'player': 'black', 'coord': {'x': 4, 'y': 0}, 'pinned': False, 'attacker': None}, 
            {'type': 'Bishop', 'player': 'black', 'coord': {'x': 5, 'y': 0}, 'pinned': False, 'attacker': None}, 
            {'type': 'Knight', 'player': 'black', 'coord': {'x': 6, 'y': 0}, 'pinned': False, 'attacker': None}, 
            {'type': 'Rook', 'player': 'black', 'coord': {'x': 7, 'y': 0}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 0, 'y': 1}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 1, 'y': 1}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 2, 'y': 1}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 3, 'y': 1}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 4, 'y': 1}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 5, 'y': 1}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 6, 'y': 1}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 7, 'y': 1}, 'pinned': False, 'attacker': None}
        ]
    }


def case_napolean_attack_board() -> dict:
    return {
        'state': 'checkmate', 
        'player': 'black', 
        'pieces': [
            {'type': 'Queen', 'player': 'white', 'coord': {'x': 5, 'y': 1}, 'pinned': False, 'attacker': None}, 
            {'type': 'Bishop', 'player': 'white', 'coord': {'x': 2, 'y': 4}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 4, 'y': 4}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 0, 'y': 6}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 1, 'y': 6}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 2, 'y': 6}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 3, 'y': 6}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 5, 'y': 6}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 6, 'y': 6}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 7, 'y': 6}, 'pinned': False, 'attacker': None}, 
            {'type': 'Rook', 'player': 'white', 'coord': {'x': 0, 'y': 7}, 'pinned': False, 'attacker': None}, 
            {'type': 'Knight', 'player': 'white', 'coord': {'x': 1, 'y': 7}, 'pinned': False, 'attacker': None}, 
            {'type': 'Bishop', 'player': 'white', 'coord': {'x': 2, 'y': 7}, 'pinned': False, 'attacker': None}, 
            {'type': 'King', 'player': 'white', 'coord': {'x': 4, 'y': 7}, 'pinned': False, 'attacker': None}, 
            {'type': 'Knight', 'player': 'white', 'coord': {'x': 6, 'y': 7}, 'pinned': False, 'attacker': None}, 
            {'type': 'Rook', 'player': 'white', 'coord': {'x': 7, 'y': 7}, 'pinned': False, 'attacker': None}, 
            {'type': 'Rook', 'player': 'black', 'coord': {'x': 0, 'y': 0}, 'pinned': False, 'attacker': None}, 
            {'type': 'Bishop', 'player': 'black', 'coord': {'x': 2, 'y': 0}, 'pinned': False, 'attacker': None}, 
            {'type': 'Queen', 'player': 'black', 'coord': {'x': 3, 'y': 0}, 'pinned': False, 'attacker': None}, 
            {'type': 'King', 'player': 'black', 'coord': {'x': 4, 'y': 0}, 'pinned': False, 'attacker': None}, 
            {'type': 'Bishop', 'player': 'black', 'coord': {'x': 5, 'y': 0}, 'pinned': False, 'attacker': None}, 
            {'type': 'Knight', 'player': 'black', 'coord': {'x': 6, 'y': 0}, 'pinned': False, 'attacker': None}, 
            {'type': 'Rook', 'player': 'black', 'coord': {'x': 7, 'y': 0}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 0, 'y': 1}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 1, 'y': 1}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 2, 'y': 1}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 6, 'y': 1}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 7, 'y': 1}, 'pinned': False, 'attacker': None}, 
            {'type': 'Knight', 'player': 'black', 'coord': {'x': 2, 'y': 2}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 3, 'y': 2}, 'pinned': False, 'attacker': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 4, 'y': 3}, 'pinned': False, 'attacker': None}
        ]
    }