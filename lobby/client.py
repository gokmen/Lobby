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
import sys

from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import ssl, reactor

from lobby.ssl.verifiedssl import VerifyingClientContextFactory

MY_NAME = "CLIENT"

class EchoClient(LineReceiver):

    def connectionMade(self):
        # self.sendLine("HAND_SHAKE")
        self.sendLine("SERVICE:listServices")
        # self.transport.loseConnection()

    def connectionLost(self, reason):
        print 'Something Happened !'

    def lineReceived(self, line):
        print 'I received :', line

    def sendLine(self, line):
        LineReceiver.sendLine(self, '|'.join((MY_NAME, line)))

class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def clientConnectionFailed(self, connector, reason):
        print 'Connection Failed:', reason.getErrorMessage()
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print 'Connection Lost:', reason.getErrorMessage()
        reactor.stop()

def main():
    factory = EchoClientFactory()

    SERVER_CERT_FILE = "ss_cert_a.pem"

    CLIENT_CERT_FILE = "ss_cert_b.pem"
    CLIENT_KEY_FILE  = "ss_key_b.pem"

    ctxFactory = VerifyingClientContextFactory(CLIENT_CERT_FILE, CLIENT_KEY_FILE)
    # The client will only connect to a server which presents this certificate.
    ctxFactory.loadAllowedCertificate(SERVER_CERT_FILE)

    reactor.connectSSL('localhost', 8000, factory, ctxFactory)
    reactor.run()

if __name__ == '__main__':
    main()
