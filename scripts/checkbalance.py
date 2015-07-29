#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 46elks AB <hello@46elks.com>
# Developed in 2015 by Emil Tullstedt <emil@46elks.com>
# Licensed under the MIT License

from __future__ import print_function
from base64 import b64encode
try:
    from urllib import urlencode
    from urllib2 import HTTPError, urlopen, Request
except ImportError:
    from urllib.parse import urlencode
    from urllib.error import HTTPError
    from urllib.request import urlopen, Request
import json
import sys



