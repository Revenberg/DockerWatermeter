#!/bin/bash

git pull
chmod +x build.sh

docker image build -t revenberg/watermeter .

# docker push revenberg/watermeter

# testing: docker run revenberg/watermeter