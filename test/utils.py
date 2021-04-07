# -*- coding: utf-8 -*-
"""Utils for package modules.

This module contains code that ensures the functionality
of the package in the sustainable way.
"""


from typing import Union
from typing import List
from typing import Any


def assert_obj_attr(obj: object, attr: str, target: object):
    """Assert a objects attribute.

    First the code will assert if the given object has the
    attribute that is to be checked. Secondly it the code
    will assert of the attributes value is the target.

    Args:
        obj (:obj:): The object whose attribute is to be checked.
        attr (str): The name of the attribute which is to be checked.
        target (:obj:): The target value of the attribute in question.
    """
    assert attr in dir(obj)
    assert getattr(obj, attr) == target


def assert_obj_func(obj: object, func: str, param: Union[List[Any], None], target: object):
    """Assert a objects function.

    First the code will assert if the given object has the
    function that is to be checked. Secondly it the code
    will assert of the functions return value is the target.

    Args:
        obj (:obj:): The object whose attribute is to be checked.
        func (str): The name of the function which is to be checked.
        param (:obj:, optional): Parameters for the function call.
        target (:obj:): The target value of the attribute in question.
    """
    assert func in dir(type(obj))

    if param:
        assert getattr(obj, func)(*param) == target
    else:
        assert getattr(obj, func)() == target