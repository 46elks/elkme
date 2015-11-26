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
from helpers import b, s, parse_payload, requires_elements

class Elks:
    username = None
    password = None
    api_url = "https://api.46elks.com/a1/%s"

    def __init__(self, conf):
        requires_elements(['username', 'password'], conf)
        self.username = conf['username']
        self.password = conf['password']

    def query_api(self, data=None, endpoint='SMS'):
        url = self.api_url % endpoint
        if data:
            conn = Request(url, b(urlencode(data)))
        else:
            conn = Request(url)

        auth = b('Basic ') + b64encode(b(self.username + ':' + self.password))
        conn.add_header('Authorization', auth)

        try:
            response = urlopen(conn)
        except HTTPError as err:
            print(err)
            print("\nSending didn't succeed :(")
            exit(-2)
        return response.read()


    def validate_number(self, number):
        if number[0] == '+':
            return True
        else:
            raise Exception("Phone number must be of format +CCCXXX...")


    def send_text(self, conf, message):
        """Sends a text message to a configuration conf containing the message
        in the message paramter"""
        if 'from' not in conf:
            conf["from"] = 'elkme'
        requires_elements(['to'], conf)
        self.validate_number(conf['to'])

        if not isinstance(message, str):
            message = " ".join(message)

        sms = {
            'from': conf["from"],
            'to': conf["to"],
            'message': message[:159]
        }

        if 'debug' in conf:
            print(sms)

        response = self.query_api(sms)

        if 'debug' in conf:
            print(s(response))
        elif 'verbose' in conf:
            retval = json.loads(s(response))

            if len(message) > 160:
                print(message)
                print('----')
                print('Sent first 160 characters to ' + retval['to'])
            else:
                print('Sent "' + retval['message'] + '" to ' + retval['to'])


    def make_call(self, conf, payload):
        requires_elements(['from', 'to'], conf)
        voice_start = parse_payload(payload)
        if 'debug' in conf:
            print(voice_start)
        call = {
            'from': conf['from'],
            'to': conf['to'],
            'voice_start': voice_start
        }
        response = self.query_api(call, 'Calls')
        if 'debug' in conf:
            print(s(response))
        elif 'verbose' in conf:
            retval = json.loads(s(response))
            print('Made connection to ' + conf['to'])


    def my_user(self, conf={'verbose': True}):
        response = self.query_api(endpoint='Me')
        if 'debug' in conf:
            print(s(response))
        elif 'verbose' in conf:
            retval = json.loads(s(response))
            for key in retval:
                print('%s: %s' % (key, retval[key]))


    def my_numbers(self, conf={'verbose': True}):
        response = self.query_api(endpoint='Numbers')
        if 'debug' in conf:
            print(s(response))
        elif 'verbose' in conf:
            numbers = json.loads(s(response))['data']
            if 'showall' in conf:
                numbers = [num['number'] for num in numbers]
            else:
                numbers = [num['number'] for num in numbers
                            if num['active'] == 'yes']
            for number in numbers:
                print(number)

