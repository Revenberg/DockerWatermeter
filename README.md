# DockerWatermeter

sudo apt install gnupg2 pass
docker image build -t DockerWatermeter  .
docker login -u revenberg
docker image push revenberg/DockerWatermeter:latest

docker run revenberg/DockerWatermeter

docker exec -it ??? /bin/sh

docker push revenberg/DockerWatermeter: