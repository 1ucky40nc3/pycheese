# -*- coding: utf-8 -*-
"""Utils for package modules.

This module contains code that ensures the functionality
of the package in the sustainable way.
"""


from typing import Type
from typing import List
from typing import Tuple
from typing import Union


class Boundary:
    """Class that is used to check if a value is in a boundary.

    Args:
        min (int): Minimal value inside boundary.
        max (int): Exclusive max value inside boundary.

    Example:
        >>> boundary = Boundary(0, 4)
        >>> boundary.accepts(0)
        True
        >>> boundary.accepts(4)
        False
    """
    def __init__(self, min: int, max: int):
        self.__min = min
        self.__max = max
    
    def accepts(self, value: int) -> bool:
        """Check if the value is inside the boundary.

        Args:
            value (int) value that shall be checked

        Returns:
            boolean: True if value is in boundary, False otherwise.
        
        Example:
        >>> boundary = Boundary(0, 4)
        >>> boundary.accepts(0)
        True
        >>> boundary.accepts(4)
        False
        """
        return value >= self.__min and value < self.__max


def coord_to_json(coord: Union[List[Tuple[int, int]], Tuple[int, int]],
                  output_list: bool = False):
    """Convert a coordinate into a JSON representation."""
    if isinstance(coord, tuple):
        coord = [coord]

    json = []
    for x, y in coord:
        json.append({"x": x, "y": y})

    if len(json) == 1 and not output_list:
        return json[0]

    return json

def normalize(x: int) -> int:
    """Normalize an integer between -1 and 1."""
    if x > 0:
        return 1
    elif x < 0:
            return -1
    return 0