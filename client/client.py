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

MY_KEY = "KEY_1"
MY_NAME= "CLIENT"

KNOWN_KEYS = ["KEY_1"]

class EchoClient(LineReceiver):

    def connectionMade(self):
        self.sendLine("HAND_SHAKE")
        # self.transport.loseConnection()

    def connectionLost(self, reason):
        print 'Something Happened !'

    def lineReceived(self, line):
        print 'I received :', line

    def sendLine(self, line):
        LineReceiver.sendLine(self, '|'.join((MY_NAME, MY_KEY, line)))

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
    reactor.connectSSL('localhost', 8000, factory, ssl.ClientContextFactory())
    reactor.run()

if __name__ == '__main__':
    main()