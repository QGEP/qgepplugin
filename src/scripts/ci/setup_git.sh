#!/bin/bash

openssl aes-256-cbc -K $encrypted_5d9ba2164160_key -iv $encrypted_5d9ba2164160_iv -in qgep_rsa.enc -out ~/.ssh/id_rsa -d
chmod 600 ~/.ssh/id_rsa;
git config --global user.email "qgep@opengis.ch";
git config --global user.name "QGEP";
git config --global push.default simple;
