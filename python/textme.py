#!/usr/bin/python
#
# Copyright (c) 2015 46elks AB <hello@46elks.com>
# Developed in 2015 by Emil Tullstedt <emil@46elks.com>
# Licensed under the MIT License
from __future__ import print_function

elk = """
  ,;MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM;,.
/MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM.
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM`   `^'  `Q/^^\MMMpcqMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM;,             `^'   `VP    YP'  `MM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMDomm;,._                     /M
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMP`        _.,,=rRMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMP^^^^MMMM'          MMMMMMMMMMMMMMMMMM
MMMMMMMMP`              '^^oMMMPP`       ``'            \MMMMMMMMMMMMMMMM
MMMMMMM'                                                  ``\MMMMMMMMMMMM
MMMMMM'                                                          'QMMMMMM
MMM/`                                                              \MMMMM
MM/_=o,                                     ,/     \_               `MMMM
MMMMMMM,                                   /MM     pMM\,._           MMMM
MMMMMMMM,                                 ,MMMM, pMMMMMMMX          /MMMM
MMMMMMMMP                                 AMMMMMMMMMMMMMMMM\m____.pMMMMMM
MMMMMMMP                                  MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMM|         ,.mPDMMMMMMMMpo.,        \MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMM|      ,mPMMMMMMMMMMMMMMMMMDo       \MMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMM|    /MMMMMMMMMMMMMMMMMMMMMMMM\       \MMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMM|    MMMMMMMMMMMMMMMMMMMMMMMMMMDp,.    `MMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMP     MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMP    \MMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMM|    `MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM|     \MMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMPPDmmMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
MMMMMMMMMMMMMMMBYMMJOHANNESLMMOFMM46ELKSMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
\MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMP
 `\MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM`
"""

helptext = """
Send a text message using the commandline powered by the 46elks
API available from https://www.46elks.com. The tool reads it's configuration 
from a colon separated file located in ~/.textme or from commandline.
textme also supports pipes
"""

usage = """Hello,
textme is a tool for sending text messages using the commandline.

To use textme, you need to have an account on 46elks <https://46elks.com> and
login to your dashboard to receive your API username and password.

Run `textme "Hello internet" -u APIUSERNAME -p APIPASSWORD -t +46700000000` to
send a text message from commandline. That's it. (oh, and don't forget to
add --saveconf so that you don't have to enter the settings every time you
run the application)

See `textme --help` for more information about textme"""

from base64 import b64encode
from urllib import urlencode
import argparse
import ConfigParser
import json
import os
import string
import sys
import urllib2

def read_config(path, section="46elks"):
    config = ConfigParser.RawConfigParser()
    try:
        config.read(path)
    except ConfigParser.MissingSectionHeaderError:
        return {}
    settings = {}
    try:
        for element in config.items(section):
            settings[element[0]] = element[1]
    except ConfigParser.NoSectionError:
        return {}
    return settings

def send_text(conf, message):
    if 'from' in conf:
        sender  = conf['from']
    else:
        sender  = 'textme'
    try:
        username = conf['username']
        password = conf['password']
        to = conf['to']
    except KeyError as e:
        print("You need to provide API username, password and a recipient",
            file=sys.stderr)
        missing = 'Error: '
        if not 'username' in conf:
            missing += "'username' "
        if not 'password' in conf:
            missing += "'password' "
        if not 'to' in conf:
            missing += "'to' " 
        print(missing, "missing")
        exit(-3)

    if to[0] != '+':
        print("Number must be of the format +CCXXXXXXXXX", file=sys.stderr)
        exit(-22)

    if type(message) != str: 
        message = string.join(message, " ")

    sms = {
        'from': sender,
        'to': to,
        'message': message[:159]
    }

    if 'debug' in conf:
        print(sms)

    auth = 'Basic ' + b64encode(username + ':' + password)
    conn = urllib2.Request("https://api.46elks.com/a1/SMS",
        urlencode(sms))
    conn.add_header('Authorization', auth)
    try:
        response = urllib2.urlopen(conn)
    except urllib2.HTTPError as e:
        print(e)
        print("\nSending didn't succeed :(")
        exit(-2)

    if 'debug' in conf:
        print(response.read())
    elif 'verbose' in conf:
        rv = json.loads(response.read())

        if len(message) > 160:
            print(message)
            print("----")
            print("Sent first 160 characters to " + rv['to'] )
        else:
            print('Sent "' + rv['message'] + '" to ' + rv['to'])

def generate_config(conf, section="46elks"):
    config = ConfigParser.RawConfigParser()
    config.add_section(section)
    if 'username' in conf:
        config.set(section, 'username', conf['username'])
    if 'password' in conf:
        config.set(section, "password", conf['password'])
    if 'to' in conf:
        config.set(section, "to", conf['to'])
    if 'from' in conf:
        config.set(section, "from", conf['from'])
    if not config.items(section):
        error  = "You need to provide options to be stored as"
        error += " commandline options"
        print(error, file=sys.stderr)
    if 'verbose' in conf:
        print("Wrote to the config file :)")
    return config

def parse_args():
    parser = argparse.ArgumentParser(
        description=helptext,
        epilog="This application is powered by elks with superpowers!")
    parser.add_argument('-v', '--verbose', action='count',
        help="Debug output")
    parser.add_argument('-q', '--quiet', action='count',
        help="Suppress most output")
    parser.add_argument('message', metavar='message', type=str, nargs='*',
        help="The message to be sent (<160 characters)")
    parser.add_argument('-f', '--file', metavar='file', action='store',
        help="""File to read message from (only the first 160 characters
            are sent)""")
    parser.add_argument('-t', '--to', dest='to', action='store',
        help="Phone number to receive the text message")
    parser.add_argument('-s', '--sender', '--from', dest='sender', 
        action='store', help="""
            Sender of the message. See 46elks' API documentation for valid
            formats
        """)
    parser.add_argument('-u', '--username', dest='username', action='store',
        help="Your API username from https://www.46elks.com/"
        )
    parser.add_argument('-p', '--password', dest='password', action='store',
        help="Your API password from https://www.46elks.com/"
        )
    parser.add_argument('--saveconf', dest='saveconf', 
        action='count', help="""
            Generates a configuration file from the commandline options and
            exits.
        """)
    parser.add_argument('-c', '--config', dest='configfile',
        help="Location of the configuration file (default ~/.textme)")
    return parser.parse_args()

def main():
    args = parse_args()

    if args.configfile:
        conffile = os.path.expanduser(args.configfile)
    else:
        conffile = os.environ['HOME'] + "/.textme"

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
        f = open(args.file, 'r')
        message = f.read()
    elif not sys.stdin.isatty():
        message = ''
        try:
            while True:
                message += raw_input()
                message += '\n'
        except EOFError as e:
            pass

    if args.saveconf:
        with open(conffile, 'w') as fdest:
            settings = generate_config(conf)
            settings.write(fdest)
        if not message:
            exit(0)

    if not message:
        print(usage, file=sys.stderr)
        exit(-1)

    if args.verbose >= 2 or (message[0:3][0] == 'elks'):
        print(elk)

    send_text(conf, message)

main()
