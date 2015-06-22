#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 46elks AB <hello@46elks.com>
# Developed in 2015 by Emil Tullstedt <emil@46elks.com>
# Licensed under the MIT License

from __future__ import print_function
from base64 import b64encode
from urllib import urlencode
import json
import urllib2
import sys

def query_api(username, password, data, endpoint="SMS"):
    auth = 'Basic ' + b64encode(username + ':' + password)
    conn = urllib2.Request("https://api.46elks.com/a1/" + endpoint,
                           urlencode(data))
    conn.add_header('Authorization', auth)
    try:
        response = urllib2.urlopen(conn)
    except urllib2.HTTPError as err:
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
        conf["from"] = 'textme'

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
        print(response)
    elif 'verbose' in conf:
        retval = json.loads(response)

        if len(message) > 160:
            print(message)
            print("----")
            print("Sent first 160 characters to " + retval['to'])
        else:
            print('Sent "' + retval['message'] + '" to ' + retval['to'])

