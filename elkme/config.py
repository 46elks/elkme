#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 46elks AB <hello@46elks.com>
# Developed in 2015 by Emil Tullstedt <emil@46elks.com>
# Licensed under the MIT License

from __future__ import print_function
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser
import sys, os, stat
import platform
from subprocess import call

template = """\
#
# elkme configuration file
#

###
# AUTHENTICATION
#
# Your API keys from https://dashboard.46elks.com goes here. Please keep
# these somewhat secret
###
{username}
{password}

###
# SENDING SMS DETAILS
#
# Set a default recipient (with the `to` key) and a default sender
# (using the `from` key). Your `to` key must be a E.163 international format
# phone number and your `from` key must either be E.163 or a valid
# alphanumerical sender (starting with letter, maximum of 11 letters/digits)
#
# The from-number should be either your own number (as you registered it on
# your 46elks account) or a 46elks number on your account.
###
{from}
{to}

###
# ROUTING
#
# If you have a mock 46elks server available for debugging purposes or a
# proxy or something, you can use the `api_url` key to route your API calls
# to it. Most people will want to leave this at it's default
###
# api_url = https://api.46elks.com/a1
"""

def init_config(args):
    status = (True, None)
    conffile = locate_config(args)
    conf = {}
    try:
        conf = read_config(conffile)
    except IOError as e:
        pass
    conf = update_config_with_args(conf, args)
    if args.saveconf:
        status = save_config(conf, conffile)

    if args.editconf:
        open_text_editor(conffile)

    return (conf, status)

def open_text_editor(destfile):
    edited = False
    editors = [
            os.environ.get('EDITOR'),
            'nano',
            'vim',
            'vi',
            'emacs',
            'gedit'
    ]
    for editor in editors:
        if not editor:
            continue

        retcode = call(['which', editor]) # Is the text editor in PATH?
        if not retcode: # UNIX returns 0 on success
            call([editor, destfile])
            edited = True
            break
    if not edited:
        print('Couldn\'t find a text editor on your system')
    else:
        print('Done editing the configuration file')
    sys.exit(0)

def locate_config(args):
    if args.configfile:
        return os.path.expanduser(args.configfile)
    else:
        return default_config_location()


def default_config_location(Filename="elkme"):
    home = os.path.expanduser('~')
    location = home + os.sep + "." + Filename

    if platform.system() == "Darwin":
        path = home + os.sep + "Library" + os.sep + "Application Support"\
                + os.sep
        location = path + Filename
    elif platform.system() == "Linux":
        path = home + os.sep + ".config" + os.sep
        location = path + Filename
        if not os.path.isdir(path):
            os.mkdir(path)
    elif platform.system() == "Windows":
        # Might break on Windows <= XP
        # That's ok, since XP is no longer supported by MSFT
        location = os.environ["LOCALAPPDATA"] + os.sep + Filename + ".ini"

    return location


def read_config(path, section="46elks"):
    settings = {}
    with open(path, 'r') as f:
        row = 0
        for line in f:
            row += 1
            line = line.strip()
            if not line or line[0] in '[#':
                continue
            line = line.split('=', 1)
            if len(line) != 2:
                print('[ERROR] Expected = delimited on line {}'.format(row))
                continue
            key = line[0].strip()
            value = line[1].strip()
            settings[key] = value
    return settings


def generate_config(conf):
    """
    Generates a configuration file using the ConfigParser library that
    can be saved to a file for subsequent reads
    """

    c = {}
    def to_key(key, default):
        if conf.get(key):
            c[key] = '{} = {}'.format(key, conf.get(key))
        else:
            c[key] = default

    to_key('username', '# username = u1234...')
    to_key('password', '# password = secret...')
    to_key('from', '# from = elkme')
    to_key('to', '# to = +46700000000')
    return (True, c)

def update_config_with_args(conf, args):
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
    return conf

def save_config(conf, conffile):
    status = None
    try:
        with open(conffile, 'w') as fdest:
            status, settings = generate_config(conf)
            fdest.write(template.format(**settings))
        # Set file permissions to 600 for the configuration file
        # (this is to prevent malicious usage of your API keys)
        os.chmod(conffile, stat.S_IRUSR | stat.S_IWUSR)
    except IOError as e:
        return (False, 'Failed updating configuration file:\n{}'.format(e))

    if status:
        print('Updated configuration file {}'.format(conffile))
    return (True, status)
