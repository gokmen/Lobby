#!/usr/bin/python
# -*- coding: utf-8 -*-

''' Lobby
    2011 - Gökmen Göksel <gokmeng:gmail.com> '''

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

# Credits Copyright (c) Twisted Matrix Laboratories

import sys
import time

from OpenSSL import SSL

from twisted.internet import ssl
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory

from lobby.ssl.verifiedssl import VerifyingServerContextFactory

from lobby.actions import ActionServices
from lobby.actions import ActionPackages

MY_NAME = "SERVER"

ACTIONS = {"SERVICE" : ActionServices(),
           "PACKAGE" : ActionPackages()}

def log(msg):
    print "LOBBY (%s) >>>", time.ctime(), msg

class Lobby(Protocol):

    delimiter = '\r\n'

    def dataReceived(self, data):
        name, action = map(lambda x: x.strip(), data.split('|',1))
        action, method = map(lambda x: x.strip(), action.split(':',1))

        # log("Data received from '%s'" % name)

        if action == "HAND_SHAKE":
            log("HAND_SHAKE suceeded with '%s'" % name)
            self.pushMessage("AUTHORIZED")
        elif action in ACTIONS:
            self.pushMessage(ACTIONS[action].run(method))
        else:
            self.pushMessage("NOT_IMPLEMENTED")

    def pushMessage(self, message):
        if type(message) in (list, tuple):
            message = ','.join(message)
        self.transport.write(str('|'.join((MY_NAME, message))) + self.delimiter)

class LobbyFactory(Factory):
    protocol = Lobby

if __name__ == '__main__':

    from twisted.python import log
    log.startLogging(sys.stdout)

    from lobby.utils import init_certificates
    from lobby.utils import get_client_certificates

    factory = LobbyFactory()

    certificate, key_file = init_certificates()
    ctxFactory = VerifyingServerContextFactory(certificate, key_file)

    # Only clients presenting this certificate are allowed
    # to connect to the server.
    for cert in get_client_certificates():
        ctxFactory.loadAllowedCertificate(cert)

    reactor.listenSSL(8000, factory, ctxFactory)
    reactor.run()

