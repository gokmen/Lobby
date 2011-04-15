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

PACKAGES = {"SERVICE" : ActionServices(),
            "PACKAGE" : ActionPackages()}

class Lobby(Protocol):

    delimiter = '\r\n'

    def dataReceived(self, data):
        data = data.strip().split('\r\n')

        for chunk in data:
            _chunk = chunk.split(';')
            package = _chunk.pop(0)
            method = '' if not _chunk else _chunk.pop(0)
            args = _chunk

            print "PROCESSING: package, method, args:", package, method, args
            if package == "HELLO":
                self.pushMessage("HELLO|HELLO")
            elif package == "HELLO|MY_NAME_IS":
                print ("HAND_SHAKE suceeded with '%s'" % method)
                self.pushMessage("HELLO|AUTHORIZED")
            elif package in PACKAGES:
                self.pushMessage(chunk, PACKAGES[package].run(method, args))
            else:
                self.pushMessage("%s|NOT_IMPLEMENTED" % chunk)

    def pushMessage(self, message, args = None):
        if type(args) in (list, tuple):
            args = ','.join(args)
        if args:
            message = '%s|%s' % (message, args)
        print "TRYING TO WRITE:::", message
        self.transport.write(str(message + self.delimiter))

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

