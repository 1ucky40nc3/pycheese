# -*- coding: utf-8 -*-
"""Unittests for code in the utils module.

This module contains code to test the content
of the pycheese.core.utils module using pytest.

Example:
    To run the tests you can for example:
        - Run the pytest command from the command line:
            ..> pytest
        - Run the tests.py file in the repos top-level:
            ..> python tests.py
"""


from pycheese.core.utils import Boundary
from pycheese.core.utils import coord_to_dict
from pycheese.core.utils import dict_to_coord

from test.utils import assert_obj_attr


def test_boundary():
    """Test the Boundary class function.

    Check if the functions's behavoir is correct.
    To do so initialize an instance of the Boundary class
    and assert the functions output with different setups.
    """
    min, max = 0, 10
    boundary = Boundary(min, max)

    # Test the attributes.
    assert_obj_attr(boundary, "min", min)
    assert_obj_attr(boundary, "max", max)

    # Test if a boundary behaves correctly with single int.
    assert boundary.accepts(min)

    for i in range(min, max):
        assert boundary.accepts(i)

    assert not boundary.accepts(max)

    # Test if a boundary behaves correctly with list of int.
    for i in range(min, max):
        for j in range(min, max):
            assert boundary.accepts([i, j])

    assert not boundary.accepts([max, max])

    assert Boundary(min, min).accepts(min)


def test_coord_to_dict():
    x, y = 0, 0

    # Test conversion of single coord.
    coord = [x, y]
    dict = {"x": x, "y": y}

    assert coord_to_dict(coord) == dict

    # Test conversion of list of coord.
    coord = [[x, y]]*2
    dict = [dict, dict]

    assert coord_to_dict(coord) == dict

    # Test special case with empty list.
    assert coord_to_dict([]) == []


def test_dict_to_coord():
    x, y = 0, 0

    # Test conversion of single dict.
    dict = {"x": x, "y": y}
    coord = [x, y]

    assert dict_to_coord(dict) == coord
    assert dict_to_coord(dict, as_list=True) == [coord]

    # Test conversion of list of coord.
    dict = [dict, dict]
    coord = [[x, y]]*2
    
    assert dict_to_coord(dict) == coord
    assert dict_to_coord(dict, as_list=True) == coord

    # Test special case with empty list.
    assert dict_to_coord([]) == []

