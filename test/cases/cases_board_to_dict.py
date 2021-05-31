# -*- coding: utf-8 -*-
"""Unittests for code in the board module.

This module contains code to test the content
of the pycheese.core.board module using pytest.
"""


def case_initial_board() -> dict:
    return {
        'state': 'ongoing', 
        'player': 'white', 
        'last': {}, 
        'pieces': [
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 0, 'y': 6}, 'options': {'moves': [{'x': 0, 'y': 5}, {'x': 0, 'y': 4}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 1, 'y': 6}, 'options': {'moves': [{'x': 1, 'y': 5}, {'x': 1, 'y': 4}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 2, 'y': 6}, 'options': {'moves': [{'x': 2, 'y': 5}, {'x': 2, 'y': 4}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 3, 'y': 6}, 'options': {'moves': [{'x': 3, 'y': 5}, {'x': 3, 'y': 4}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 4, 'y': 6}, 'options': {'moves': [{'x': 4, 'y': 5}, {'x': 4, 'y': 4}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 5, 'y': 6}, 'options': {'moves': [{'x': 5, 'y': 5}, {'x': 5, 'y': 4}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 6, 'y': 6}, 'options': {'moves': [{'x': 6, 'y': 5}, {'x': 6, 'y': 4}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 7, 'y': 6}, 'options': {'moves': [{'x': 7, 'y': 5}, {'x': 7, 'y': 4}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Rook', 'player': 'white', 'coord': {'x': 0, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Knight', 'player': 'white', 'coord': {'x': 1, 'y': 7}, 'options': {'moves': [{'x': 0, 'y': 5}, {'x': 2, 'y': 5}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Bishop', 'player': 'white', 'coord': {'x': 2, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Queen', 'player': 'white', 'coord': {'x': 3, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'King', 'player': 'white', 'coord': {'x': 4, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Bishop', 'player': 'white', 'coord': {'x': 5, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Knight', 'player': 'white', 'coord': {'x': 6, 'y': 7}, 'options': {'moves': [{'x': 5, 'y': 5}, {'x': 7, 'y': 5}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Rook', 'player': 'white', 'coord': {'x': 7, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Rook', 'player': 'black', 'coord': {'x': 0, 'y': 0}, 'options': {'moves': [{'x': 0, 'y': 1}, {'x': 1, 'y': 0}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Knight', 'player': 'black', 'coord': {'x': 1, 'y': 0}, 'options': {'moves': [{'x': 0, 'y': 2}, {'x': 2, 'y': 2}, {'x': 3, 'y': 1}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Bishop', 'player': 'black', 'coord': {'x': 2, 'y': 0}, 'options': {'moves': [{'x': 1, 'y': 1}, {'x': 3, 'y': 1}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Queen', 'player': 'black', 'coord': {'x': 3, 'y': 0}, 'options': {'moves': [{'x': 3, 'y': 1}, {'x': 4, 'y': 0}, {'x': 2, 'y': 0}, {'x': 2, 'y': 1}, {'x': 4, 'y': 1}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'King', 'player': 'black', 'coord': {'x': 4, 'y': 0}, 'options': {'moves': [{'x': 4, 'y': 1}, {'x': 5, 'y': 0}, {'x': 3, 'y': 0}, {'x': 3, 'y': 1}, {'x': 5, 'y': 1}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Bishop', 'player': 'black', 'coord': {'x': 5, 'y': 0}, 'options': {'moves': [{'x': 4, 'y': 1}, {'x': 6, 'y': 1}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Knight', 'player': 'black', 'coord': {'x': 6, 'y': 0}, 'options': {'moves': [{'x': 5, 'y': 2}, {'x': 7, 'y': 2}, {'x': 4, 'y': 1}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Rook', 'player': 'black', 'coord': {'x': 7, 'y': 0}, 'options': {'moves': [{'x': 7, 'y': 1}, {'x': 6, 'y': 0}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 0, 'y': 1}, 'options': {'moves': [{'x': 1, 'y': 2}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 1, 'y': 1}, 'options': {'moves': [{'x': 0, 'y': 2}, {'x': 2, 'y': 2}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 2, 'y': 1}, 'options': {'moves': [{'x': 1, 'y': 2}, {'x': 3, 'y': 2}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 3, 'y': 1}, 'options': {'moves': [{'x': 2, 'y': 2}, {'x': 4, 'y': 2}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 4, 'y': 1}, 'options': {'moves': [{'x': 3, 'y': 2}, {'x': 5, 'y': 2}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 5, 'y': 1}, 'options': {'moves': [{'x': 4, 'y': 2}, {'x': 6, 'y': 2}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 6, 'y': 1}, 'options': {'moves': [{'x': 5, 'y': 2}, {'x': 7, 'y': 2}], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'Pawn', 'player': 'black', 'coord': {'x': 7, 'y': 1}, 'options': {'moves': [{'x': 6, 'y': 2}], 'others': []}, 'pinned': False, 'pinner': None}
        ]
    }


def case_napoleon_attack_board() -> dict:
    return {
        'state': 'checkmate', 
        'player': 'black',
        'last': {},
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


def case_rook_checkmate_board():
    return {
        'state': 'ongoing',
        'player': 'black',
        'last': {},
        'pieces': [
            {'type': 'Rook', 'player': 'white', 'coord': {'x': 0, 'y': 1}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
            {'type': 'Rook', 'player': 'white', 'coord': {'x': 1, 'y': 1}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
            {'type': 'King', 'player': 'white', 'coord': {'x': 7, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'King', 'player': 'black', 'coord': {'x': 7, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}
        ]
    }


def case_queen_check_empty_board():
    return  {
        'state': 'ongoing',
        'player': 'white', 
        'last': {},
        'pieces': [
            {'type': 'Queen', 'player': 'white', 'coord': {'x': 3, 'y': 6}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
            {'type': 'King', 'player': 'white', 'coord': {'x': 4, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'King', 'player': 'black', 'coord': {'x': 4, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}
        ]
    }


def case_and_king_queen_stalemate_board():
    return {
        'state': 'ongoing', 
        'player': 'white',
        'last': {},
        'pieces': [
            {'type': 'Queen', 'player': 'white', 'coord': {'x': 0, 'y': 1}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'King', 'player': 'white', 'coord': {'x': 6, 'y': 2}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
            {'type': 'King', 'player': 'black', 'coord': {'x': 7, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}
        ]
    }


def case_promotion_empty_board():
    return {
        'state': 'ongoing', 
        'player': 'white',
        'last': {},
        'pieces': [
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 0, 'y': 1}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'King', 'player': 'white', 'coord': {'x': 6, 'y': 2}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
            {'type': 'King', 'player': 'black', 'coord': {'x': 7, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}
        ]
    }


def case_promotion_checkmate_empty_board():
    return {
        'state': 'ongoing', 
        'player': 'white',
        'last': {},
        'pieces': [
            {'type': 'Pawn', 'player': 'white', 'coord': {'x': 0, 'y': 1}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'King', 'player': 'white', 'coord': {'x': 6, 'y': 2}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
            {'type': 'King', 'player': 'black', 'coord': {'x': 7, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}
        ]
    }


def case_check_by_castle_board():
    return {
        'state': 'ongoing', 
        'player': 'white',
        'last': {},
        'pieces': [
            {'type': 'Rook', 'player': 'white', 'coord': {'x': 7, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}, 
            {'type': 'King', 'player': 'white', 'coord': {'x': 4, 'y': 7}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None},
            {'type': 'King', 'player': 'black', 'coord': {'x': 5, 'y': 0}, 'options': {'moves': [], 'others': []}, 'pinned': False, 'pinner': None}
        ]
    }