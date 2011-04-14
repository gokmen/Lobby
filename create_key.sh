#!/usr/bin/env sh

# ATTRIBUTION:
# See http://www.madboa.com/geek/openssl/#cert-self

openssl req \
  -x509 -nodes -days 365 \
  -subj '/C=TR/ST=NA/L=Istanbul/CN=pardus.org.tr' \
  -newkey rsa:1024 -keyout my_key.pem -out my_cert.pem

