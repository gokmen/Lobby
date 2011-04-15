#!/usr/bin/python
# -*- coding: utf-8 -*-

''' Lobby
    2011 - Gökmen Göksel <gokmeng:gmail.com> '''

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

from lobby.client import LobbyClient

# Create a LobbyClient instance
client = LobbyClient()

# Set remote host certificate
client.loadServerCertificate("/path/to/remote/system/certificate/remote_cert.pem")

# Create connection for given IP:PORT
client.connectSSL("192.168.1.1", 8000)

# To get list of services
client.addMessageToQueue('SERVICE;listServices')

# To query status of openssh service
client.addMessageToQueue('SERVICE;isRunning;openssh')

# Run the client loop
client.run()

# Print the received data for given messages
print "RECEIVED_DATA:", client._received_data

