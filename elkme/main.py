#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 46elks AB <hello@46elks.com>
# Developed in 2015 by Emil Tullstedt <emil@46elks.com>
# Licensed under the MIT License

"""
elkme is a commandline utility to send sms from the terminal
"""

from __future__ import print_function
from .config import read_config, generate_config, default_config_location
from .elks import Elks
import argparse
import os
import sys
import json
from .helpers import b, s

ELK = """
  ,;MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM;,.
/MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM.
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM`   `^'  `Q/^^\\MMMpcqMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM;,             `^'   `VP    YP'  `MM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMDomm;,._                     /M
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMP`        _.,,=rRMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMP^^^^MMMM'          MMMMMMMMMMMMMMMMMM
MMMMMMMMP`              '^^oMMMPP`       ``'            \\MMMMMMMMMMMMMMMM
MMMMMMM'                                                  ``\\MMMMMMMMMMMM
MMMMMM'                                                          'QMMMMMM
MMM/`                                                              \\MMMMM
MM/_=o,                                     ,/     \\_               `MMMM
MMMMMMM,                                   /MM     pMM\\,._           MMMM
MMMMMMMM,                                 ,MMMM, pMMMMMMMX          /MMMM
MMMMMMMMP                                 AMMMMMMMMMMMMMMMM\\m____.pMMMMMM
MMMMMMMP                                  MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMM|         ,.mPDMMMMMMMMpo.,        \\MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMM|      ,mPMMMMMMMMMMMMMMMMMDo       \\MMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMM|    /MMMMMMMMMMMMMMMMMMMMMMMM\\       \\MMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMM|    MMMMMMMMMMMMMMMMMMMMMMMMMMDp,.    `MMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMP     MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMP    \\MMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMM|    `MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM|     \\MMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMPPDmmMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMBYMMJOHANNESLMMOFMM46ELKSMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
\\MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMP
 `\\MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM`
"""

HELPTEXT = """
Send a text message using the commandline powered by the 46elks
API available from https://www.46elks.com.
textme also supports pipes
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


def main():
    """Executed on run"""

    try:
        input = raw_input
    except NameError:
        pass

    args = parse_args()

    if args.configfile:
        conffile = os.path.expanduser(args.configfile)
    else:
        conffile = default_config_location()

    conf = read_config(conffile)

    if args.quiet < 1:
        conf['verbose'] = True
    if args.verbose >= 1 and args.quiet < 1:
        conf['debug'] = True
    if args.to:
        conf['to'] = args.to
    if args.sender:
        conf['from'] = args.sender
    if args.username:
        conf['username'] = args.username
    if args.password:
        conf['password'] = args.password

    message = None
    if args.message and not args.file:
        message = args.message
    elif args.file:
        with open(args.file, 'r') as openfile:
            message = openfile.read()
    elif not sys.stdin.isatty():
        message = ''
        try:
            while True:
                message += input()
                message += '\n'
        except EOFError:
            pass

    if args.saveconf:
        try:
            with open(conffile, 'w') as fdest:
                settings = generate_config(conf)
                settings.write(fdest)
        except IOError as e:
            print(e)
        if not message:
            exit(0)

    invalid_conf = False
    try:
      elks_conn = Elks(conf)
    except KeyError:
      invalid_conf = True

    if args.me:
        elks_conn.list_user()
        exit(0)
    if args.numbers:
        if not message:
          message = ''
        numbers = elks_conn.list_numbers(all = 'all' in message)
        for i, number in enumerate(numbers):
          print("(%s) %s" % (i, number))
        exit(0)

    if not message:
        print(USAGE, file=sys.stderr)
        exit(-1)

    if args.verbose >= 2 or (message[0:3][0] == 'elks'):
        print(ELK)

    if invalid_conf:
      print(USAGE, file=sys.stderr)
      print("\n\nYour configuration is invalid", file=sys.stderr)
      exit(-1)

    if args.call:
        response = elks_conn.make_call(message,
            conf.get('to', None),
            conf.get('from', None))
        if 'debug' in conf:
            print(s(response))
        elif 'verbose' in conf:
            retval = json.loads(s(response))
            print('Made connection to ' + conf['to'])
    else:
        send_sms(elks_conn, conf, message)

def parse_args():
    """Parse the arguments to the application"""
    parser = argparse.ArgumentParser(
        description=HELPTEXT,
        epilog="This application is powered by elks with superpowers!")
    parser.add_argument('-v', '--verbose', action='count',
                        help="Debug output", default=0)
    parser.add_argument('-q', '--quiet', action='count',
                        help="Suppress most output", default=0)
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
    parser.add_argument('--saveconf', dest='saveconf',
                        action='count', help="""
                        Generates a configuration file from the commandline
                        options and exits.""")
    parser.add_argument('-c', '--config', dest='configfile',
                        help="""Location of the custom configuration file""")
    parser.add_argument('--call', '--dial', action='store_true', default=False,
                        help="""Make a call""")
    parser.add_argument('--me', action='store_true', help="User info")
    parser.add_argument('--numbers', action='store_true',
                        help="Show my numbers")
    return parser.parse_args()

def send_sms(conn, conf, message):
    sender = conf.get('from', 'elkme')
    to = conf.get('to', None)

    response = conn.send_sms(message[:159], to, sender)

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

if __name__ == '__main__':
    main()

