#!/bin/bash

# Exit on error
set -e

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/../..


if [ ! -z "$TRAVIS_TAG" ] && [ "$TRAVIS_PULL_REQUEST" == "false" ];
then
  VERSION=$(echo "${TRAVIS_TAG}" | sed -e 's/v\([0-9]\.]*\)/\1/')
  echo "Deploy version ${VERSION} now..."

  ${DIR}/scripts/ci/setup_git.sh
  pushd ${DIR}
  git clone git@github.com:QGEP/repository.git
  cd repository
  ../scripts/make-qgep-release.sh ${VERSION}

  popd
fi
