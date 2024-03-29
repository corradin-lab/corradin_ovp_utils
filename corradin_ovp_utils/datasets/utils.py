# AUTOGENERATED! DO NOT EDIT! File to edit: 06_utils.ipynb (unless otherwise specified).

__all__ = ['MissingAttributeError', 'requires', 'cd']

# Cell
from typing import Any, Dict, List, Optional, Literal, Union
from pydantic import BaseModel
import corradin_ovp_utils
from fastcore.basics import typed
from fastcore.dispatch import typedispatch

# Cell

class MissingAttributeError(Exception):
    pass

def requires(*required_attrs):
    def wrapper(method):

        @functools.wraps(method)
        def inner_wrapper(self, *args, **kargs):
            if not all(hasattr(self, attr) for attr in required_attrs):
                raise MissingAttributeError()
            return method(self, *args, **kargs)

        return inner_wrapper
    return wrapper


from contextlib import contextmanager
import os

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)