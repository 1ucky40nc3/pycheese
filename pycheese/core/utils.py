# -*- coding: utf-8 -*-
"""Utils for package modules.

This module contains code that ensures the functionality
of the package in the sustainable way.
"""


from typing import Union
from typing import List


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
        self.min = min
        self.max = max
    
    def accepts(self, value: Union[int, List[int]]) -> bool:
        """Check if the value is inside the boundary.

        Args:
            value (int) value that shall be checked

        Returns:
            boolean: True if value is in boundary, False otherwise.
        
        Example:
        >>> boundary = Boundary(0, 4)
        >>> boundary.accepts(0)
        True
        >>> boundary.accepts((0, 0))
        True
        >>> boundary.accepts(4)
        False
        """
        if isinstance(value, int):
            value = [value]

        in_boundary = [v in range(self.min, self.max) for v in value]

        return all(in_boundary)


def coord_to_dict(coord: Union[List[List[int]], List[int]], 
                  as_list: bool = False) -> Union[List[dict], dict]:
    """Convert a coordinate into a JSON representation."""
    json = []

    # Check if list of coord is empty.
    if not coord:
        return json
    
    # Check if list of coord is passed as arg.
    if isinstance(coord[0], int):
        coord = [coord]

    for x, y in coord:
        json.append({"x": x, "y": y})

    # Return a single dict if conditions meet.
    if len(json) == 1 and not as_list:
        return json[0]

    return json


def dict_to_coord(json: Union[List[dict], dict], 
                  as_list: bool = False) -> Union[List[List[int]], List[int]]:
    """Convert a coordinate in JSON representation into the internal."""
    coord = []

    # Check if list of coord is empty.
    if not json:
        return coord

    # Check if list of dict is passed as arg.
    if isinstance(json, dict):
        json = [json]

    for i in json:
        x, y = i["x"], i["y"]
        coord.append([x, y])

    # Return a single coord if conditions meet.
    if len(coord) == 1 and not as_list:
        return coord[0]

    return coord


def normalize(x: int) -> int:
    """Normalize an integer between -1 and 1."""
    if x > 0:
        return 1
    elif x < 0:
            return -1
    return 0