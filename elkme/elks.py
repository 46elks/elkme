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
from helpers import b, s

def query_api(username, password, data, endpoint="SMS"):
    conn = Request("https://api.46elks.com/a1/" + endpoint,
                           b(urlencode(data)))

    auth = b('Basic ') + b64encode(b(username + ':' + password))
    conn.add_header('Authorization', auth)
        
    try:
        response = urlopen(conn)
    except HTTPError as err:
        print(err)
        print("\nSending didn't succeed :(")
        exit(-2)
    return response.read()

def validate_number(number):
    if number[0] == '+':
        return True
    else:
        raise Exception("Invalid phonenumber. Must be of format +CCXXXXXXXX")

def send_text(conf, message):
    """Sends a text message to a configuration conf containing the message in
    the message paramter"""
    if not 'from' in conf:
        conf["from"] = 'elkme'

    missing = ''
    if 'username' not in conf:
        missing += "'username' "
    if 'password' not in conf:
        missing += "'password' "
    if 'to' not in conf:
        missing += "'to' "
    if missing:
        print("You need to provide API username, password and a recipient",
            file=sys.stderr)
        print("Error:", missing, "missing", file=sys.stderr)
        exit(-3)

    validate_number(conf["to"])

    if not isinstance(message, str):
        message = " ".join(message)

    sms = {
        'from': conf["from"],
        'to': conf["to"],
        'message': message[:159]
    }

    if 'debug' in conf:
        print(sms)

    response = query_api(conf["username"], conf["password"], sms)

    if 'debug' in conf:
        print(s(response))
    elif 'verbose' in conf:
        retval = json.loads(s(response))

        if len(message) > 160:
            print(message)
            print("----")
            print("Sent first 160 characters to " + retval['to'])
        else:
            print('Sent "' + retval['message'] + '" to ' + retval['to'])

