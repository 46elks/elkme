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
    if 'verbose' in conf:
        print("Wrote to the config file :)")
    return config

