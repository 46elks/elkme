#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015-2017 46elks AB <hello@46elks.com>
# Developed in 2015, 2016, 2017 by Emil Tullstedt <emil@46elks.com>
# Licensed under the MIT License

"""
elkme is a commandline utility to send sms from the terminal
"""

from __future__ import print_function
import elkme.config as config
from .elks import Elks, ElksException
from requests.exceptions import HTTPError
import argparse
import os
import sys
import json

HELPTEXT = """
Send a text message using the commandline powered by the 46elks
API available from https://www.46elks.com.
elkme also supports pipes
"""

USAGE = """Hello,
elkme is a tool for sending text messages using the commandline.

To use elkme, you need to have an account on 46elks at https://46elks.com and
login to your dashboard to receive your API username and password.

Run `elkme "Hello internet" -u APIUSERNAME -p APIPASSWORD -t +46700000000` to
send a text message from commandline. That's it. (oh, and don't forget to
add --saveconf so that you don't have to enter the settings every time you
run the application)

See `elkme --help` for more information about elkme"""

small_elk = """\
                                    \W/
                                    co\ 
                                      OOOOO´
                                      || /\ """

errors = []

def main():
    """Executed on run"""

    args = parse_args()
    if args.version:
        from .__init__ import __version__, __release_date__
        print('elkme %s (release date %s)' % (__version__, __release_date__))
        print('(c) 2015-2017 46elks AB <hello@46elks.com>')
        print(small_elk)
        exit(0)

    conf, conf_status = config.init_config(args)
    if not conf_status[0]:
        errors.append(conf_status[1])
    elif conf_status[1]:
        print(conf_status[1])

    message = parse_message(args)
    if conf_status[1] and not message:
        # No message but the configuration file was stored
        sys.exit(0)

    try:
        elks_conn = Elks(auth = (conf['username'], conf['password']),
                api_url = conf.get('api_url'))
    except KeyError:
        errors.append('API keys not properly set. Please refer to ' +
            '`elkme --usage`, `elkme --help` or ' +
            'https://46elks.github.io/elkme')

    if not message:
        print(USAGE, file=sys.stderr)
        exit(-1)

    for error in errors:
        print('[ERROR] {}'.format(error))
        exit(-1)
    
    options = []
    if args.flash:
        options.append('flashsms')

    try:
        send_sms(elks_conn, conf, message, length=args.length, options=options)
    except ElksException as e:
        print(e, file=sys.stderr)

def parse_args():
    """Parse the arguments to the application"""
    parser = argparse.ArgumentParser(
        description=HELPTEXT,
        epilog="This application is powered by elks with superpowers!")
    parser.add_argument('--version', action='store_true',
                        help="Display elkme version and exit")
    parser.add_argument('-v', '--verbose', action='count',
                        help="Debug output", default=0)
    parser.add_argument('message', metavar='message', type=str, nargs='*',
                        help="The message to be sent (<160 characters)")
    parser.add_argument('-f', '--file', metavar='file', action='store',
                        help="""File to read message from (only the
                        first 160 characters are sent)""")
    parser.add_argument('-t', '--to', dest='to', action='store',
                        help="Phone number to receive the text message")
    parser.add_argument('-s', '--sender', '--from', dest='sender',
                        action='store', help="""
                        Sender of the message. See 46elks' API documentation
                        for valid formats""")
    parser.add_argument('-u', '--username', dest='username', action='store',
                        help="Your API username from https://www.46elks.com/")
    parser.add_argument('-p', '--password', dest='password', action='store',
                        help="Your API password from https://www.46elks.com/")
    parser.add_argument('--flash', action='store_true',
                        help="Send SMS as a flash-SMS")
    parser.add_argument('-l', '--length', metavar='length',
            action='store', type=int, default=160,
            help='Maximum length of the message')
    parser.add_argument('-c', '--config', dest='configfile',
                        help="""Location of the custom configuration file""")
    parser.add_argument('--saveconf', dest='saveconf',
                        action='count', help="""
                        Generates a configuration file from the commandline
                        options and exits.""")
    parser.add_argument('--editconf', action='store_true', help="""
                        Opens the configuration file in your $EDITOR""")
    return parser.parse_args()

def send_sms(conn, conf, message, length=160, options=[]):
    sender = conf.get('from', 'elkme')
    to = conf.get('to', None)

    if length > 1530 or length < 0:
        print('Length must be larger than 0 and smaller than 1530')
        return

    if not isinstance(message, str):
        message = " ".join(message)

    try:
        response = conn.send_sms(message[:length], to, sender, options=options)
    except HTTPError as e:
        print(e)
        return

    if 'debug' in conf:
        print(response)
    elif 'verbose' in conf:
        retval = json.loads(response)

        if len(message) > length:
            print(message)
            print('----')
            print('Sent first %s characters to %s' % (length, retval['to']))
        else:
            print('Sent "' + retval['message'] + '" to ' + retval['to'])

def parse_message(args):
    message = None
    if args.file: # Read from file
        with open(args.file, 'r') as openfile:
            message = openfile.read()
    elif args.message: # Message in argument
        message = " ".join(args.message)
    elif not sys.stdin.isatty(): # Pipe support
        try:
            io_in = raw_input # Python 2
        except NameError:
            io_in = input # Python 3

        message = ''
        try:
            while True:
                message += io_in()
                message += '\n'
        except EOFError:
            pass

    return message

if __name__ == '__main__':
    main()

