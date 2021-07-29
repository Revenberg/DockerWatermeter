#!/bin/bash

git pull
chmod +x build.sh

docker image build -t revenberg/watermeter .

# docker push revenberg/watermeter

# testing: 

echo "==========================================================="
echo "=                                                         ="
echo "=          docker run revenberg/watermeter                ="
echo "=                                                         ="
echo "==========================================================="
docker run revenberg/watermeter