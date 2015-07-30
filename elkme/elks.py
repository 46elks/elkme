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
from helpers import b, s, parse_payload


def query_api(username, password, data, endpoint='SMS'):
    api_url = "https://api.46elks.com/a1/%s" % endpoint
    if data:
        conn = Request(api_url, b(urlencode(data)))
    else:
        conn = Request(api_url)

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
    if 'from' not in conf:
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


def make_call(conf, payload):
    voice_start = parse_payload(payload)
    if 'debug' in conf:
        print(voice_start)

    try:
        call = {
            'from': conf['from'],
            'to': conf['to'],
            'voice_start': voice_start
        }

        response = query_api(conf['username'], conf['password'], call, 'Calls')
        if 'debug' in conf:
            print(s(response))
        elif 'verbose' in conf:
            retval = json.loads(s(response))
            print('Made connection to ' + conf['to'])
    except KeyError as e:
        print('Missing one or more arguments necessary to make a connection:')
        print(e)


def my_user(conf):
    response = query_api(conf['username'], conf['password'], None, 'Me')
    if 'debug' in conf:
        print(s(response))
    elif 'verbose' in conf:
        retval = json.loads(s(response))
        for key in retval:
            print('%s: %s' % (key, retval[key]))
    return s(response)


def my_numbers(conf):
    response = query_api(conf['username'], conf['password'], None, 'Numbers')
    if 'debug' in conf:
        print(s(response))
    elif 'verbose' in conf:
        retval = json.loads(s(response))
        if 'showall' in conf:
            numbers = retval['data']
        else:
            numbers = filter(lambda num: num['active'] == 'yes', retval['data'])
        numbers = list(map(lambda num: num['number'], numbers))
        for number in numbers:
            print(number)
    return s(response)

