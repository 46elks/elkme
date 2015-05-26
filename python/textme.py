#!/usr/bin/python

from base64 import b64encode
from urllib import urlencode
import argparse
import json
import os
import string
import sys
import urllib2

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
API <https://www.46elks.com>. The tool reads it's configuration from a
colon separated file located in ~/.textme or from commandline
"""

def read_config(path):
    settings = {}
    try:
        with open(path, 'r') as f:
            for line in f:
                line = line.split(":")
                line[-1] = line[-1][:-1] # Remove the new-line character
                settings[line[0]] = (line[1])
    except IOError:
        pass
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
        print "You need to provide API username, password and a recipient"
        missing = 'Error: '
        if not 'username' in conf:
            missing += "'username' "
        if not 'password' in conf:
            missing += "'password' "
        if not 'to' in conf:
            missing += "'to' " 
        print missing + " missing"
        exit(-3)

    if type(message) != str: 
        message = string.join(message, " ")

    sms = {
        'from': sender,
        'to': to,
        'message': message[:159]
    }

    if 'debug' in conf:
        print sms

    auth = 'Basic ' + b64encode(username + ':' + password)
    conn = urllib2.Request("https://api.46elks.com/a1/SMS",
        urlencode(sms))
    conn.add_header('Authorization', auth)
    try:
        response = urllib2.urlopen(conn)
    except urllib2.HTTPError as e:
        print e
        print "\nSending didn't succeed :("
        exit(-2)

    if 'debug' in conf:
        print response.read()
    elif 'verbose' in conf:
        rv = json.loads(response.read())
        print 'Sent "' + rv['message'] + '" to ' + rv['to']

def generate_config(username, password, to, sender):
    if username:
        print "username:" + username
    if password:
        print "password:" + password
    if to:
        print "to:" + to
    if sender:
        print "from:" + sender

def parse_args():
    parser = argparse.ArgumentParser(
        description=helptext,
        epilog="This application is powered by elks with superpowers!")
    parser.add_argument('-v', '--verbose', action='count',
        help="Verbose output")
    parser.add_argument('-vv', '--debug', action='count',
        help="Debug output")
    parser.add_argument('message', metavar='message', type=str, nargs='*',
        help="The message to be sent, reads a maximum of 160 characters")
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
        help="""
            Your API username from https://dashboard.46elks.com/
            Reads from ~/.textme if not supplied
        """
        )
    parser.add_argument('-p', '--password', dest='password', action='store',
        help="""
            Your API password from https://dashboard.46elks.com/
            Reads from ~/.textme if not supplied
        """
        )
    parser.add_argument('--generateconf', dest='generateconf', action='count',
        help="""
            Prints a configuration file for textme with your options to
            standard output and the exits without sending a message
        """)
    return parser.parse_args()

def main():
    args = parse_args()
    conf = read_config(os.environ['HOME'] + "/.textme")


    if args.verbose >= 1:
        conf['verbose'] = True
    if args.verbose >= 2 or args.debug:
        conf['debug'] = True
    if args.to:
        conf['to'] = args.to
    if args.sender:
        conf['from'] = args.sender
    if args.username:
        conf['username'] = args.username
    if args.password:
        conf['password'] = args.password
    if args.generateconf:
        generate_config(args.username, args.password, args.to, args.sender)
        exit(0)

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

    if args.verbose >= 3 or (message[0:3][0] == 'elks'):
        print elk

    send_text(conf, message)

main()
