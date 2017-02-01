# -*- coding: utf-8 -*-

from gevent.monkey import patch_all; patch_all()

import sys


if sys.version_info <= (3, 5):
    raise RuntimeError('Support for 3.5 and greater version of python')


del sys, patch_all
