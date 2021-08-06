#!/bin/bash

git pull
chmod +x build.sh

docker image build -t revenberg/dockerwatermeter .

docker push revenberg/dockerwatermeter

# testing: 

echo "==========================================================="
echo "=                                                         ="
echo "=          docker run revenberg/dockerwatermeter                ="
echo "=                                                         ="
echo "==========================================================="
# docker run revenberg/dockerwatermeter