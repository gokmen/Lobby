#!/usr/bin/python
# -*- coding: utf-8 -*-

''' Lobby
    2011 - Gökmen Göksel <gokmeng:gmail.com> '''

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

# Copyright (C) 2005 Darrell Karbott (djk2005 at users dot sf dot net)
# This code is free software; you can redistribute it and/or modify
# it under the terms of the GNU Public Licence (GPL) version 2 See
# http://www.gnu.org/ for further details of the GPL.

from OpenSSL import SSL, crypto
from twisted.internet import ssl

# Cribbed from M2Crypto cb.py which,
# Cribbed from OpenSSL's apps/s_cb.c.

# from ssl.h
SSL_ST_CONNECT = 0x1000
SSL_ST_ACCEPT  = 0x2000
SSL_ST_MASK    = 0x0FFF

SSL_CB_LOOP    = 0x01
SSL_CB_EXIT    = 0x02
SSL_CB_READ    = 0x04
SSL_CB_WRITE   = 0x08
SL_CB_ALERT    = 0x4000

def ssl_info_callback(connection, where, ret):
    # ssl_conn = Connection.map()[ssl_ptr]
    # sys.stdout.write(ssl_ptr + ':' + str(sys.getrefcount(ssl_conn)) + '\n')
    # sys.stdout.flush()

    w = where & ~SSL_ST_MASK
    if (w & SSL_ST_CONNECT):
        state = "SSL connect"
    elif (w & SSL_ST_ACCEPT):
        state = "SSL accept"
    else:
        state = "SSL state unknown"

    if (where & SSL_CB_LOOP):
        # sys.stderr.write("LOOP: %s: %s\n" % (state, m2.ssl_get_state_v(ssl_ptr)))
        print "LOOP: %s: %s\n" % (state, connection.state_string())
        return

    if (where & SSL_CB_EXIT):
        if not ret:
            print "FAILED: %s: %s\n" % (state, connection.state_string())
        else:
            print "INFO: %s: %s\n" % (state, connection.state_string())
        return

    # I don't think this code would ever execute under pyOpenSSL because
    # it handles alerts with exception, but I'm not sure.
    if (where & SSL_CB_ALERT):
        if (where & SSL_CB_READ):
            w = 'read'
        else:
            w = 'write'
        # sys.stderr.write("ALERT: %s: %s: %s\n" % \
        #     (w, m2.ssl_get_alert_type_v(ret), m2.ssl_get_alert_desc_v(ret)))
        print "ALERT: %s: DUNNO HOW TO GET ALERT INFO!\n" % \
            (w)
        return

class VerifyingBase:

    def __init__(self, ownCertFile, ownKeyFile):
        self.allowedCertificates = []
        bytes = file(ownCertFile).read()
        self.ownCert = crypto.load_certificate(crypto.FILETYPE_PEM, bytes)
        bytes = file(ownKeyFile).read()
        self.ownKey = crypto.load_privatekey(crypto.FILETYPE_PEM, bytes)

    # NOTE: Doesn't add the certificate to existing contexts.
    def loadAllowedCertificate(self, fileName):
        bytes = file(fileName).read()
        self.allowedCertificates.append(crypto.load_certificate(crypto.FILETYPE_PEM, bytes))

    def addAllowedCertificatesToContext(self, ctx):
        store = ctx.get_cert_store()
        for cert in self.allowedCertificates:
            store.add_cert(cert)

    # initialization which is the same for both client and server.
    def initContext(self, ctx):
        ctx.use_certificate(self.ownCert)
        ctx.use_privatekey(self.ownKey)
        self.addAllowedCertificatesToContext(ctx)
        ctx.set_verify(SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT, self.verify_certificate)
        ctx.set_info_callback(ssl_info_callback)
        return ctx

    def verify_certificate(self, conn, cert, errno, depth, retcode):
        # UNDOCUMENTED:
        # retcode is non-zero if the built in verification code would
        # succeed, false otherwise.
        print "verify_certificate: ", cert, errno, depth, retcode

        # UNDOCUMENTED:
        # See http://divmod.org/websvn/wsvn/Quotient/trunk/mantissa/sslverify.py?op=file&rev=0&sc=0
        # _errorcodes for errno descriptions. 
        if not retcode:
            print "VERIFICATION FAILED: ", errno

        return retcode

class VerifyingClientContextFactory(ssl.ClientContextFactory, VerifyingBase):
    def getContext(self):
        return self.initContext(SSL.Context(self.method))

class VerifyingServerContextFactory(VerifyingBase):
    def getContext(self):
        return self.initContext(SSL.Context(SSL.SSLv23_METHOD))

