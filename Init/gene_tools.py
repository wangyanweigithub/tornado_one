# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'
import sys
import os

def get_current_file_path():
    path = sys.path[0]
    if os.path.isdir(path):
        path = os.path.dirname(path)
        return path
    elif os.path.isfile(path):
        path = os.path.dirname(path)
        return os.path.dirname(path)


def init_path():
    path = get_current_file_path()
    sys.path.append(path)

