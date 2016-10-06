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
from requests.exceptions import HTTPError
import argparse
import os
import sys
import json

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

small_elk = """\
                                    \W/
                                    co\ 
                                      OOOOO´
                                      || /\ """

def main():
    """Executed on run"""

    try:
        io_in = raw_input
    except NameError:
        io_in = input

    args = parse_args()
    if args.version:
        from .__init__ import __version__, __release_date__
        print('elkme %s (release date %s)' % (__version__, __release_date__))
        print('(c) 2015-2016 46elks AB <hello@46elks.com>')
        print(small_elk)
        exit(0)

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
    if args.message and not args.file: # Message in argument
        message = args.message
    elif args.file: # Read file support
        with open(args.file, 'r') as openfile:
            message = openfile.read()
    elif not sys.stdin.isatty(): # Pipe support
        message = ''
        try:
            while True:
                message += io_in()
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
      elks_conn = Elks(auth = (conf['username'], conf['password']),
              api_url = conf.get('api_url'))
    except KeyError:
      invalid_conf = True

    if not message:
        print(USAGE, file=sys.stderr)
        exit(-1)

    if args.verbose >= 2 or (message[0:3][0] == 'elks'):
        print(ELK)

    if invalid_conf:
      print(USAGE, file=sys.stderr)
      print("\n\nInvalid configuration", file=sys.stderr)
      exit(-1)

    send_sms(elks_conn, conf, message, length=args.length)

def parse_args():
    """Parse the arguments to the application"""
    parser = argparse.ArgumentParser(
        description=HELPTEXT,
        epilog="This application is powered by elks with superpowers!")
    parser.add_argument('--version', action='store_true',
                        help="Display elkme version and exit")
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
    parser.add_argument('-l', '--length', metavar='length',
            action='store', type=int, default=160,
            help='Maximum length of the message')
    parser.add_argument('-c', '--config', dest='configfile',
                        help="""Location of the custom configuration file""")
    return parser.parse_args()

def send_sms(conn, conf, message, length=160):
    sender = conf.get('from', 'elkme')
    to = conf.get('to', None)

    if length > 1530 or length < 0:
        print('Length must be larger than 0 and smaller than 1530')
        return

    if not isinstance(message, str):
        message = " ".join(message)

    try:
        response = conn.send_sms(message[:length], to, sender)
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

if __name__ == '__main__':
    main()

