# -*- coding: utf-8 -*-

import sys


if sys.version_info <= (3, 5):
    raise RuntimeError('Support for 3.5 and greater version of python')
