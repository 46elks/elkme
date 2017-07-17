#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015-2017 46elks AB <hello@46elks.com>
# Developed in 2015-2017 by Emil Tullstedt <emil@46elks.com>
# Licensed under the MIT License

from __future__ import (print_function, division, unicode_literals)

gsm7 =  u"@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞÆæßÉ !\"#¤%&'()*+,-./0123456789:;<=>?¡"
gsm7 += u"ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿abcdefghijklmnopqrstuvwxyzäöñüà"

def number_of_sms(message):
    """
    The number of parts that will be used to send this specific SMS
    """
    utf16 = not is_gsm7(message)

    # FIXME: Ensure everything is unicode at this point for both Py2 and Py3

    if utf16:
        return len(message.encode('utf-16be'))//2*67+1
    else:
        return len(message)//153+1

def is_gsm7(message):
    """
    Returns true if message is in the GSM 03.38 default 7-bit alphabet

    >>> is_gsm7('Hello, world')
    True

    >>> is_gsm7('€')
    False
    """
    for char in message:
        if char not in gsm7:
            return True
    return False

