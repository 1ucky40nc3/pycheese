# -*- coding: utf-8 -*-
"""Custom errors.

This module contains code to be able to raise custom
errors and exceptios by the package in the sustainable way.
"""

class PyCheeseException(Exception):
    pass
class NotInPlayersPossesionException(PyCheeseException):
    pass
class MoveNotLegalException(PyCheeseException):
    pass