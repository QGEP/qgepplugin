#!/bin/bash

# Exit on error
set -e

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/../..


if [ ! -z "$TRAVIS_TAG" ] && [ "$TRAVIS_PULL_REQUEST" == "false" ];
then
  echo "Deploy now..."

  ${DIR}/scripts/ci/setup_git.sh
  pushd ${DIR}
  git clone git@github.com:QGEP/repository.git
  cd repository
  ../scripts/make-qgep-release.sh ${TRAVIS_TAG}

  popd
fi
