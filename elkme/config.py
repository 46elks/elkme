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
import sys
import os
import platform
from subprocess import call

def init_config(args):
    status = (None, None)
    conffile = locate_config(args)
    conf = read_config(conffile)
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
    """Reads configuration from a configuration file using the
    ConfigParser library"""
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


def generate_config(conf, section="46elks"):
    """
    Generates a configuration file using the ConfigParser library that
    can be saved to a file for subsequent reads
    """
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
        error = "You need to provide options to be stored as"
        error += " commandline options"
        print(error, file=sys.stderr)
        return (False, config)
    return (True, config)

def update_config_with_args(conf, args):
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
    return conf

def save_config(conf, conffile):
    status = None
    try:
        with open(conffile, 'w') as fdest:
            status, settings = generate_config(conf)
            settings.write(fdest)
    except IOError as e:
        return (False, 'Failed updating configuration file:\n{}'.format(e))

    if status:
        print('Updated configuration file {}'.format(conffile))
    return (True, status)
