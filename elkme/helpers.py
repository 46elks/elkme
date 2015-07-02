#!/usr/bin/env python

import sys

if sys.version_info < (3,):
    def b(x):
        return x
    def s(x):
        return x
else:
    def b(x):
        return bytes(x, 'utf-8')
    def s(x):
        return x.decode('utf-8')

