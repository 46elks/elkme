#!/usr/bin/python

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

import urllib2
import sys
import string
import os
import argparse
from urllib import urlencode
from base64 import b64encode

def read_config(path):
    f = open(path, 'r')
    settings = {}
    for line in f:
        line = line.split(":")
        line[-1] = line[-1][:-1] # Remove the new-line character
        settings[line[0]] = (line[1])
    return settings

def send_text(conf, message):
    username    = conf['username']
    password    = conf['password']
    if 'from' in conf:
        sender  = conf['from']
    else:
        sender  = 'textme'
    to   = conf['to']

    if type(message) != str: 
        message = string.join(message, " ")

    sms = {
        'from': sender,
        'to': to,
        'message': message[:159]
    }

    if 'verbosity' in conf:
        print sms

    auth = 'Basic ' + b64encode(username + ':' + password)
    conn = urllib2.Request("https://api.46elks.com/a1/SMS",
        urlencode(sms))
    conn.add_header('Authorization', auth)
    response = urllib2.urlopen(conn)
    print response.read()

def parse_args():
    parser = argparse.ArgumentParser(
        description=
            """
            Send a text message using the commandline powered by the 46elks
            API <https://www.46elks.com>
            """,
        epilog="This application is powered by elks with superpowers!")
    parser.add_argument('-v', '--verbose', action='count')
    parser.add_argument('message', metavar='message', type=str, nargs='*',
        help="The message to be sent, maximum 160 characters")
    parser.add_argument('-f', '--file', metavar='file', action='store',
        help="File to read message from, maximum 160 characters")
    parser.add_argument('-t', '--to', dest='to', action='store',
        help="Phone number to receive the text message")
    parser.add_argument('-s', '--sender', '--from', dest='sender', 
        action='store', help="""
            The sender of the message.
            This could be either a phone number associated to your 
            46elks-account or a string with a character [a-zA-Z] followed
            by up to seven alphanumerical characters [0-9a-zA-Z]
        """)
    parser.add_argument('-u', '--username', dest='username', action='store',
        help="Your API username from https://dashboard.46elks.com/"
        )
    parser.add_argument('-p', '--password', dest='password', action='store',
        help="Your API password from https://dashboard.46elks.com/"
        )
    return parser.parse_args()

args = parse_args()
conf = read_config(os.environ['HOME'] + "/.textme")

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
        print e
else:
    print "No message provided. Please consult " + sys.argv[0] + " --help"
    exit(-1)

if args.verbose >= 1:
    conf['verbosity'] = True
if args.verbose >= 2 or (message[0:3][0] == 'elks'):
    print elk
if args.to:
    conf['to'] = args.to
if args.sender:
    conf['from'] = args.sender
if args.username:
    conf['username'] = args.username
if args.password:
    conf['password'] = args.password

send_text(conf, message)
