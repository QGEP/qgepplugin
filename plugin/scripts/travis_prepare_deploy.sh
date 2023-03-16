#!/bin/bash
if [ "$TRAVIS_SECURE_ENV_VARS" == "true" ];
then
	openssl aes-256-cbc -K $encrypted_5d9ba2164160_key -iv $encrypted_5d9ba2164160_iv -in github_deploy_key.enc -out github_deploy_key.out -d
	chmod 600 github_deploy_key.out
	eval $(ssh-agent -s)
	ssh-add github_deploy_key.out
fi
sed -ie 's/git@github.com:/https:\/\/github.com\//' .gitmodules
git submodule update --init --recursive
