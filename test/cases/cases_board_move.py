# -*- coding: utf-8 -*-
"""Unittests for code in the board module.

This module contains code to test the content
of the pycheese.core.board module using pytest.
"""


def case_napoleon_attack() -> dict:
    """Test case for the boards `move` funtion.
    
    To test the function the follow chess game will be played:
    1. e4 e5 2. Qf3 Nc6 3. Bc4 d6 4. Qxf7#
    """
    return [
        {
            "source_coord": [4, 6],
            "target_coord": [4, 4],
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 4, 'y': 6}, 
                'target_coord': {'x': 4, 'y': 4}, 
                'event': {'extra': 'unique', 'type': 'move'}
            }
        },
        {
            "source_coord": [4, 1],
            "target_coord": [4, 3],
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 4, 'y': 1}, 
                'target_coord': {'x': 4, 'y': 3}, 
                'event': {'extra': 'unique', 'type': 'move'}
            }
        },
        {
            "source_coord": [3, 7],
            "target_coord": [5, 5],
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 3, 'y': 7}, 
                'target_coord': {'x': 5, 'y': 5}, 
                'event': {'extra': 'unique', 'type': 'move'}
            }
        },
        {
            "source_coord": [1, 0],
            "target_coord": [2, 2],
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 1, 'y': 0}, 
                'target_coord': {'x': 2, 'y': 2}, 
                'event': {'extra': 'unique', 'type': 'move'}
            }
        },
        {
            "source_coord": [5, 7],
            "target_coord": [2, 4],
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 5, 'y': 7}, 
                'target_coord': {'x': 2, 'y': 4}, 
                'event': {'extra': 'unique', 'type': 'move'}
            }
        },
        {
            "source_coord": [3, 1],
            "target_coord": [3, 2],
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 3, 'y': 1}, 
                'target_coord': {'x': 3, 'y': 2}, 
                'event': {'extra': 'unique', 'type': 'move'}
            }
        },
        {
            "source_coord": [5, 5],
            "target_coord": [5, 1],
            "promotion_target": None,
            "output": {
                'state': 'checkmate', 
                'source_coord': {'x': 5, 'y': 5}, 
                'target_coord': {'x': 5, 'y': 1}, 
                'event': {'type': 'captures', 'extra': "unique"}
            }
        },
    ]


def case_castle_kingside() -> dict:
    """Test case for the boards `move` funtion.
    
    To test the function the follow chess game will be played:
    1. Nf3 Nf6 2. e3 e6 3. Be2 Be7 4. O-O O-O
    """
    return [
        {
            "source_coord": [6, 7],
            "target_coord": [5, 5],
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 6, 'y': 7}, 
                'target_coord': {'x': 5, 'y': 5}, 
                'event': {'extra': 'unique', 'type': 'move'}
            }
        },
        {
            "source_coord": [6, 0],
            "target_coord": [5, 2],
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 6, 'y': 0}, 
                'target_coord': {'x': 5, 'y': 2}, 
                'event': {'extra': 'unique', 'type': 'move'}
            }
        },
        {
            "source_coord": [4, 6],
            "target_coord": [4, 5],
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 4, 'y': 6}, 
                'target_coord': {'x': 4, 'y': 5}, 
                'event': {'extra': 'unique', 'type': 'move'}
            }
        },
        {
            "source_coord": [4, 1],
            "target_coord": [4, 2],
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 4, 'y': 1}, 
                'target_coord': {'x': 4, 'y': 2}, 
                'event': {'extra': 'unique', 'type': 'move'}
            }
        },
        {
            "source_coord": [5, 7],
            "target_coord": [4, 6],
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 5, 'y': 7}, 
                'target_coord': {'x': 4, 'y': 6}, 
                'event': {'extra': 'unique', 'type': 'move'}
            }
        },
        {
            "source_coord": [5, 0],
            "target_coord": [4, 1],
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 5, 'y': 0}, 
                'target_coord': {'x': 4, 'y': 1}, 
                'event': {'extra': 'unique', 'type': 'move'}
            }
        },
        {
            "source_coord": [4, 7],
            "target_coord": [6, 7],
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 4, 'y': 7}, 
                'target_coord': {'x': 6, 'y': 7}, 
                'event': {'type': 'castle', 'extra': 'kingside'}
            }
        },
        {
            "source_coord": [4, 0],
            "target_coord": [6, 0],
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 4, 'y': 0}, 
                'target_coord': {'x': 6, 'y': 0}, 
                'event': {'type': 'castle', 'extra': 'kingside'}
            }
        },
    ]


def case_castle_queenside() -> dict:
    """Test case for the boards `move` funtion.
    
    To test the function the follow chess game will be played:
    1. Nc3 Nc6 2. d3 d6 3. Be3 Be6 4. Qd2 Qd7 5. O-O-O O-O-O
    """
    return [
        {
            "source_coord": [1, 7],
            "target_coord": [2, 5],
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 1, 'y': 7}, 
                'target_coord': {'x': 2, 'y': 5}, 
                'event': {'extra': 'unique', 'type': 'move'}
            }
        },
        {
            "source_coord": [1, 0],
            "target_coord": [2, 2],
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 1, 'y': 0}, 
                'target_coord': {'x': 2, 'y': 2}, 
                'event': {'extra': 'unique', 'type': 'move'}
            }
        },
        {
            "source_coord": [3, 6],
            "target_coord": [3, 5],
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 3, 'y': 6}, 
                'target_coord': {'x': 3, 'y': 5}, 
                'event': {'extra': 'unique', 'type': 'move'}
            }
        },
        {
            "source_coord": [3, 1],
            "target_coord": [3, 2],
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 3, 'y': 1}, 
                'target_coord': {'x': 3, 'y': 2}, 
                'event': {'extra': 'unique', 'type': 'move'}
            }
        },
        {
            "source_coord": [2, 7],
            "target_coord": [4, 5],
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 2, 'y': 7}, 
                'target_coord': {'x': 4, 'y': 5}, 
                'event': {'extra': 'unique', 'type': 'move'}
            }
        },
        {
            "source_coord": [2, 0],
            "target_coord": [4, 2],
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 2, 'y': 0}, 
                'target_coord': {'x': 4, 'y': 2}, 
                'event': {'extra': 'unique', 'type': 'move'}
            }
        },
        {
            "source_coord": [3, 7],
            "target_coord": [3, 6],
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 3, 'y': 7}, 
                'target_coord': {'x': 3, 'y': 6}, 
                'event': {'extra': 'unique', 'type': 'move'}
            }
        },
        {
            "source_coord": [3, 0],
            "target_coord": [3, 1],
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 3, 'y': 0}, 
                'target_coord': {'x': 3, 'y': 1}, 
                'event': {'extra': 'unique', 'type': 'move'}
            }
        },
        {
            "source_coord": [4, 7],
            "target_coord": [2, 7],
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 4, 'y': 7}, 
                'target_coord': {'x': 2, 'y': 7}, 
                'event': {'type': 'castle', 'extra': 'queenside'}
            }
        },
        {
            "source_coord": [4, 0],
            "target_coord": [2, 0],
            "promotion_target": None,
            "output": {
                'state': 'ongoing', 
                'source_coord': {'x': 4, 'y': 0}, 
                'target_coord': {'x': 2, 'y': 0}, 
                'event': {'type': 'castle', 'extra': 'queenside'}
            }
        },
    ]