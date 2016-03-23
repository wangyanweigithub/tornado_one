# -*- coding: utf-8 -*-
__author__ = 'wangyanwei'

import hashlib
import base64

def md5(text):
    return hashlib.md5(text.encode()).hexdigest()


def base64_encode(text):
    return base64.b64encode(text.encode()).decode()


def base64_decode(text):
    return base64.b64decode(text).decode()