#!/usr/bin/env python3

import re
import os
from os import path
from importlib import import_module

# builtin packages
from . import base
from . import utils


class ParseError(Exception):
    pass


class Map:

    def __init__(self):
        files = (path.basename(f) for f in os.listdir(path.dirname(__file__)))
        modules = filter(lambda f: re.match(r'_[a-zA-Z0-9]+\.py', f), files)
        # import modules & convert to dict
        self.modules = dict([(m[1:-3].upper(), import_module('.'+m[:-3], __name__)) for m in modules])

    def __getitem__(self, key):
        return getattr(self.modules[key.upper()], 'nodalize')

    def get(self, key, default=base.nodalize):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default


__map__ = Map()


def get(*args, **kwargs):
    def _decorator(nodalize):
        def _wrapper(name):
            try:
                return nodalize(name)
            except Exception as e:
                raise ParseError(f'{name}: {e}')
        return _wrapper

    return _decorator(__map__.get(*args, **kwargs))
