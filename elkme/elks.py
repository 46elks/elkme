#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 46elks AB <hello@46elks.com>
# Developed in 2015 by Emil Tullstedt <emil@46elks.com>
# Licensed under the MIT License

from __future__ import print_function
from base64 import b64encode
import requests
from requests.exceptions import HTTPError
import json
import sys
from .helpers import parse_payload

class Elks:
    auth = None
    api_url = "https://api.46elks.com/a1/%s"

    def __init__(self, auth=None, api_url=None):
        self.auth = auth
        if api_url:
            self.api_url = '%s/' % api_url + '%s'

    def query_api(self, data=None, endpoint='SMS'):
        url = self.api_url % endpoint
        if data:
            response = requests.post(
                url,
                data=data,
                auth=self.auth
            )
        else:
            response = requests.get(
                url,
                auth=self.auth
            )
        try:
            response.raise_for_status()
        except HTTPError as e:
            raise HTTPError('HTTP %s\n%s' %
                    (response.status_code, response.text))
        return response.text


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

