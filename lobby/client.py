#!/usr/bin/python
# -*- coding: utf-8 -*-

''' Lobby
    2011 - Gökmen Göksel <gokmeng:gmail.com> '''

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

# Credits Copyright (c) Twisted Matrix Laboratories

import os
import sys
from OpenSSL import SSL

from lobby.utils import get_server_addr
from lobby.utils import init_certificates
from lobby.utils import get_server_certificate

from twisted.internet import ssl, reactor
from twisted.internet.error import ReactorNotRunning
from twisted.internet.protocol import ClientFactory

from twisted.protocols.basic import LineReceiver

from lobby.ssl.verifiedssl import VerifyingClientContextFactory

MY_NAME = "CLIENT"

class LobbyClientReceiver(LineReceiver):

    def connectionMade(self):
        self.sendLine("HELLO")
        # self.sendLine("SERVICE:listServices")
        # self.transport.loseConnection()

    def connectionLost(self, reason):
        print 'Something Happened !'

    def lineReceived(self, line):
        if line.startswith('HELLO'):
            self.sendLine('MY_NAME_IS:%s' % os.getenv('HOSTNAME'))
        # print 'I received :', line

class LobbyClientFactory(ClientFactory):
    protocol = LobbyClientReceiver

    def clientConnectionFailed(self, connector, reason):
        print 'Connection Failed:', reason.getErrorMessage()
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print 'Connection Lost:', reason.getErrorMessage()
        try:
            reactor.stop()
        except ReactorNotRunning:
            pass

class LobbyClient(object):

    def __init__(self):
        certificate, key_file = init_certificates()
        self.ctx_factory = VerifyingClientContextFactory(certificate, key_file)
        self.factory = LobbyClientFactory()

    def loadServerCertificate(self, certificate):
        self.ctx_factory.loadAllowedCertificate(certificate)

    def connectSSL(self, server, port):
        reactor.connectSSL(server, int(port), self.factory, self.ctx_factory)

    def run(self):
        reactor.run()

    def sendMessage(self, message):
        self.factory.protocol.sendLine("SERVICE:listServices")

def main():

    if len(sys.argv) < 4:
        sys.exit('Usage: %s SERVER_IP SERVER_PORT SERVER_CERT_FILE' % sys.argv[0])

    from twisted.python import log
    log.startLogging(sys.stdout)

    client = LobbyClient()
    client.loadServerCertificate(sys.argv[3])
    client.connectSSL(sys.argv[1], sys.argv[2])
    client.run()

if __name__ == '__main__':
    main()
