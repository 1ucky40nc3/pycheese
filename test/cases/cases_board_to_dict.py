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
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 0, 'y': 6}, 'options': {'moves': [[0, 5], [0, 4]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 1, 'y': 6}, 'options': {'moves': [[1, 5], [1, 4]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 2, 'y': 6}, 'options': {'moves': [[2, 5], [2, 4]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 3, 'y': 6}, 'options': {'moves': [[3, 5], [3, 4]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 4, 'y': 6}, 'options': {'moves': [[4, 5], [4, 4]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 5, 'y': 6}, 'options': {'moves': [[5, 5], [5, 4]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 6, 'y': 6}, 'options': {'moves': [[6, 5], [6, 4]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 7, 'y': 6}, 'options': {'moves': [[7, 5], [7, 4]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Rook', 'player': 'white', 'coord': {'x': 0, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Knight', 'player': 'white', 'coord': {'x': 1, 'y': 7}, 'options': {'moves': [[0, 5], [2, 5]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Bishop', 'player': 'white', 'coord': {'x': 2, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Queen', 'player': 'white', 'coord': {'x': 3, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'King', 'player': 'white', 'coord': {'x': 4, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Bishop', 'player': 'white', 'coord': {'x': 5, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Knight', 'player': 'white', 'coord': {'x': 6, 'y': 7}, 'options': {'moves': [[5, 5], [7, 5]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Rook', 'player': 'white', 'coord': {'x': 7, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Rook', 'player': 'black', 'coord': {'x': 0, 'y': 0}, 'options': {'moves': [[0, 1], [1, 0]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Knight', 'player': 'black', 'coord': {'x': 1, 'y': 0}, 'options': {'moves': [[0, 2], [2, 2], [3, 1]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Bishop', 'player': 'black', 'coord': {'x': 2, 'y': 0}, 'options': {'moves': [[1, 1], [3, 1]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Queen', 'player': 'black', 'coord': {'x': 3, 'y': 0}, 'options': {'moves': [[3, 1], [4, 0], [2, 0], [2, 1], [4, 1]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'King', 'player': 'black', 'coord': {'x': 4, 'y': 0}, 'options': {'moves': [[4, 1], [5, 0], [3, 0], [3, 1], [5, 1]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Bishop', 'player': 'black', 'coord': {'x': 5, 'y': 0}, 'options': {'moves': [[4, 1], [6, 1]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Knight', 'player': 'black', 'coord': {'x': 6, 'y': 0}, 'options': {'moves': [[5, 2], [7, 2], [4, 1]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Rook', 'player': 'black', 'coord': {'x': 7, 'y': 0}, 'options': {'moves': [[7, 1], [6, 0]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 0, 'y': 1}, 'options': {'moves': [[1, 2]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 1, 'y': 1}, 'options': {'moves': [[0, 2], [2, 2]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 2, 'y': 1}, 'options': {'moves': [[1, 2], [3, 2]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 3, 'y': 1}, 'options': {'moves': [[2, 2], [4, 2]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 4, 'y': 1}, 'options': {'moves': [[3, 2], [5, 2]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 5, 'y': 1}, 'options': {'moves': [[4, 2], [6, 2]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 6, 'y': 1}, 'options': {'moves': [[5, 2], [7, 2]], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 7, 'y': 1}, 'options': {'moves': [[6, 2]], 'others': []}, 'pinned': False, 'pinner': None}
        ]
    }


def case_napoleon_attack_board() -> dict:
    return {
        'state': 'checkmate', 
        'player': 'black', 
        'pieces': [
            {'type': 'Queen', 'player': 'white', 'coord': {'x': 5, 'y': 1}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Bishop', 'player': 'white', 'coord': {'x': 2, 'y': 4}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 4, 'y': 4}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 0, 'y': 6}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 1, 'y': 6}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 2, 'y': 6}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 3, 'y': 6}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 5, 'y': 6}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 6, 'y': 6}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 7, 'y': 6}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Rook', 'player': 'white', 'coord': {'x': 0, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Knight', 'player': 'white', 'coord': {'x': 1, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Bishop', 'player': 'white', 'coord': {'x': 2, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'King', 'player': 'white', 'coord': {'x': 4, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Knight', 'player': 'white', 'coord': {'x': 6, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Rook', 'player': 'white', 'coord': {'x': 7, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Rook', 'player': 'black', 'coord': {'x': 0, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Bishop', 'player': 'black', 'coord': {'x': 2, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Queen', 'player': 'black', 'coord': {'x': 3, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'King', 'player': 'black', 'coord': {'x': 4, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Bishop', 'player': 'black', 'coord': {'x': 5, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Knight', 'player': 'black', 'coord': {'x': 6, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Rook', 'player': 'black', 'coord': {'x': 7, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 0, 'y': 1}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 1, 'y': 1}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 2, 'y': 1}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 6, 'y': 1}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 7, 'y': 1}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Knight', 'player': 'black', 'coord': {'x': 2, 'y': 2}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 3, 'y': 2}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 4, 'y': 3}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}
        ]
    }


def case_queen_check_empty_board():
    return  {
        'state': 'ongoing',
        'player': 'white', 
        'pieces': [
            {'type': 'Queen', 'player': 'white', 'coord': {'x': 3, 'y': 6}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
            {'type': 'King', 'player': 'white', 'coord': {'x': 4, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'King', 'player': 'black', 'coord': {'x': 4, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}
        ]
    }