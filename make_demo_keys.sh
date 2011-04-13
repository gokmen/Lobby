#!/usr/bin/env sh

# ATTRIBUTION:
# See http://www.madboa.com/geek/openssl/#cert-self

# This script generates the self-signed cert / key pairs
# referenced in echoserv_ssl.py and echoclient_ssl.py

openssl req \
  -x509 -nodes -days 365 \
  -subj '/C=TR/ST=NA/L=Istanbul/CN=pardus.org.tr' \
  -newkey rsa:1024 -keyout ss_key_a.pem -out ss_cert_a.pem
mv ss_key_a.pem server/
cp ss_cert_a.pem client/
mv ss_cert_a.pem server/

openssl req \
  -x509 -nodes -days 365 \
  -subj '/C=TR/ST=NA/L=Istanbul/CN=pardus.org.tr' \
  -newkey rsa:1024 -keyout ss_key_b.pem -out ss_cert_b.pem
mv ss_key_b.pem client/
cp ss_cert_b.pem server/
mv ss_cert_b.pem client/

openssl req \
  -x509 -nodes -days 365 \
  -subj '/C=TR/ST=NA/L=Istanbul/CN=pardus.org.tr' \
  -newkey rsa:1024 -keyout ss_key_c.pem -out ss_cert_c.pem
mv ss_key_c.pem client/
cp ss_cert_c.pem server/
mv ss_cert_c.pem client/

openssl req \
  -x509 -nodes -days 365 \
  -subj '/C=TR/ST=NA/L=Istanbul/CN=pardus.org.tr' \
  -newkey rsa:1024 -keyout ss_key_d.pem -out ss_cert_d.pem
mv ss_key_d.pem client/
cp ss_cert_d.pem server/
mv ss_cert_d.pem client/

