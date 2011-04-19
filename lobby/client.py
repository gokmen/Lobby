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
from OpenSSL import SSL

from lobby.utils import log
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
        for message in self.factory.message_queue:
            self.sendLine(message)

    def connectionLost(self, reason):
        log('Something Happened !')

    def lineReceived(self, line):
        if line.startswith('HELLO|HELLO'):
            self.sendLine('HELLO|MY_NAME_IS;%s' % os.getenv('HOSTNAME'))
        else:
            package, reply = line.strip().split('|')
            self.factory.received_data[package] = reply
            if package == self.factory.wait_package_reply:
                self.transport.loseConnection()

class LobbyClientFactory(ClientFactory):
    protocol = LobbyClientReceiver
    message_queue = ["HELLO"]
    received_data = {}
    wait_package_reply = ''

    def addMessageToQueue(self, message, dieAfterReply):
        self.message_queue.append(message)
        if dieAfterReply:
            self.wait_package_reply = message

    def clientConnectionFailed(self, connector, reason):
        log('Connection Failed:', reason.getErrorMessage())
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        log('Connection Lost:', reason.getErrorMessage())
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

    def run(self, message = None):
        if message:
            self.factory.addMessageToQueue(message)
        reactor.run()
        self._received_data = self.factory.received_data

    def addMessageToQueue(self, message, dieAfterReply = False):
        self.factory.addMessageToQueue(message, dieAfterReply)

if __name__ == '__main__':

    import os
    import sys

    if len(sys.argv) < 5:
        sys.exit('Usage: %s SERVER_IP SERVER_PORT SERVER_CERT_FILE COMMAND\n'
                 'Example: %s 127.0.0.1 8000 /path/remote.cert "SERVICE;isRunning;openssh"\n' % (sys.argv[0], sys.argv[0]))

    if os.getenv('LOBBY_SHOW_LOGS'):
        from twisted.python import log as twisted_log
        twisted_log.startLogging(sys.stdout)

    # Create a LobbyClient instance
    client = LobbyClient()

    # Set remote host certificate
    client.loadServerCertificate(sys.argv[3])

    # Create connection for given IP:PORT
    client.connectSSL(sys.argv[1], sys.argv[2])

    # Send given query
    client.addMessageToQueue(sys.argv[4], dieAfterReply = True)

    # Run the client loop
    client.run()

    # Print the received data for given messages
    print client._received_data

