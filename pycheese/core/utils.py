# -*- coding: utf-8 -*-
"""Utils for package modules.

This module contains code that ensures the functionality
of the package in the sustainable way.
"""


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
    
    def accepts(self, value: int):
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


