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
from .helpers import b, s, parse_payload

class Elks:
    username = None
    password = None
    api_url = "https://api.46elks.com/a1/%s"

    def __init__(self, conf={}):
        default_base_url = 'https://api.46elks.com/a1'
        self.username = conf.get('username', None)
        self.password = conf.get('password', None)
        self.api_url = '%s/' % (conf.get('api_url', default_base_url)) + '%s'

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
        if not isinstance(number, str):
            raise Exception('Phone number may not be empty')
        if number[0] == '+' and len(number) > 2 and len(number) < 16:
            return True
        else:
            raise Exception("Phone number must be of format +CCCXXX...")


    def format_sms_payload(self, message, to, sender='elkme', options=[]):
        self.validate_number(to)

        if not isinstance(message, str):
            message = " ".join(message)

        message = message.rstrip()

        sms = {
            'from': sender,
            'to': to,
            'message': message
        }
        
        for option in options:
          if option not in ['dontlog', 'dryrun', 'flash']:
            raise Exception('Option %s not supported' % option)
          sms[option] = 'yes'

        return sms

    def send_sms(self, message, to, sender='elkme', options=[]):
        """Sends a text message to a configuration conf containing the message
        in the message paramter"""
        sms = self.format_sms_payload(message=message,
            to=to,
            sender=sender,
            options=options)
        return self.query_api(sms)

    def format_call_payload(self, payload, to, sender):
        voice_start = parse_payload(payload)

        call = {
            'from': sender,
            'to': to,
            'voice_start': voice_start
        }
        return call

    def make_call(self, payload, to, sender):
        call = self.format_call_payload(payload, to, sender)
        return self.query_api(call, 'Calls')

    def list_user(self):
        response = self.query_api(endpoint='Me')
        return json.loads(s(response))

    def list_numbers(self, all = False):
        response = self.query_api(endpoint='Numbers')
        numbers = json.loads(s(response))['data']
        if not all:
            numbers = filter(lambda num: num['active'] == 'yes', numbers)
        numbers = map(lambda num: num['number'], numbers)
        return list(numbers)

