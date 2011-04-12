#!/usr/bin/python
# -*- coding: utf-8 -*-

''' Lobby
    2011 - Gökmen Göksel <gokmeng:gmail.com> '''

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

# Credits Copyright (c) Twisted Matrix Laboratories

from OpenSSL import SSL

from twisted.internet import ssl
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory

from actions import ActionServices
from actions import ActionPackages

MY_KEY = "KEY_1"
MY_NAME= "SERVER"

KNOWN_KEYS = ["KEY_1", "KEY_2", "KEY_3"]
ACTIONS = {"SERVICE" : ActionServices(),
           "PACKAGE" : ActionPackages()}

def log(msg):
    print "LOBBY >>>", msg

class ServerContextFactory:
    def getContext(self):

        ctx = SSL.Context(SSL.SSLv23_METHOD)
        ctx.use_certificate_file('cert.pem')
        ctx.use_privatekey_file('cert.pem')

        return ctx

class Echo(Protocol):

    def dataReceived(self, data):
        name, key, action = map(lambda x: x.strip(), data.split('|',2))
        log("Data received from '%s'" % name)

        if self.checkKey(key):
            log("Key check suceeded !")
            if action == "HAND_SHAKE":
                log("HAND_SHAKE suceeded with '%s'" % name)
                self.transport.write(str('|'.join((MY_NAME, MY_KEY, "AUTHORIZED"))))
        else:
            log("Key check failed !")

    def checkKey(self, key):
        log("Checking key... ")
        # Poor Man's check
        return key in KNOWN_KEYS

class EchoFactory(Factory):
    protocol = Echo

if __name__ == '__main__':

    # from twisted.python import log
    # log.startLogging(sys.stdout)

    factory = EchoFactory()
    reactor.listenSSL(8000, factory, ServerContextFactory())
    reactor.run()

