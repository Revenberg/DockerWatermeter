#!/bin/bash

git pull
chmod +x build.sh

docker image build -t revenberg/DockerWatermeter .

docker push revenberg/DockerWatermeter

# testing: 

echo "==========================================================="
echo "=                                                         ="
echo "=          docker run revenberg/DockerWatermeter                ="
echo "=                                                         ="
echo "==========================================================="
# docker run revenberg/DockerWatermeter