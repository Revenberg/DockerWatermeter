# watermeter

sudo apt install gnupg2 pass
docker image build -t watermeter  .
docker login -u revenberg
docker image push revenberg/watermeter:latest

docker run revenberg/solarwatermeterlogger


docker exec -it ??? /bin/sh

docker push revenberg/watermeter: