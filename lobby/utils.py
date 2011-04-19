#!/usr/bin/python
# -*- coding: utf-8 -*-

''' Lobby
    2011 - Gökmen Göksel <gokmeng:gmail.com> '''

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

import sys
import glob

from os import mkdir
from os import getenv
from os.path import join
from os.path import expanduser
from os.path import exists

_root = expanduser('~/.lobby')
_certificates = join(_root, 'certificates')

def init_certificates():
    if not exists(_root):
        mkdir(_root)
    if not exists(_certificates):
        mkdir(_certificates)

    _root_cert = join(_root, 'my_cert.pem')
    _root_key = join(_root, 'my_key.pem')

    if not exists(_root_cert) or not exists(_root_key):
        sys.exit('No certificate found at %s\nExiting...' % _root)

    return _root_cert, _root_key

def get_client_certificates():
    if not exists(_certificates):
        return []

    return glob.glob(join(_certificates, '*.pem'))

def get_server_certificate():
    _server_certificate = join(_root, 'server_cert.pem')
    if not exists(_server_certificate):
        sys.exit('Server certificate does not exists at %s !\nExiting...' % _root)

    return _server_certificate

def get_server_addr():
    _server_addr = join(_root, 'server_addr')
    if not exists(_server_addr):
        sys.exit('Server configuration file does not exists at %s !\nExiting...' % _root)

    return file(_server_addr).read().split(':')

def log(*message):
    if getenv('LOBBY_SHOW_LOGS'):
        print message
    return

