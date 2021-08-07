#!/bin/bash

# version 2021-08-07 15:20

cd ~/dockerwatermeter

rc=$(git remote show origin |  grep "local out of date" | wc -l)

if [ $rc -ne "0" ]; then
    git pull
    chmod +x build.sh

    docker image build -t revenberg/watermeter .

    docker push revenberg/watermeter

    # testing: 

    echo "==========================================================="
    echo "=                                                         ="
    echo "=          docker run revenberg/watermeter                ="
    echo "=                                                         ="
    echo "==========================================================="
    # docker run revenberg/watermeter
fi