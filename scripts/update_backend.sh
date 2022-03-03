git pull
docker build -t infostream-bahnapi .
docker stop infostream-bahnapi
docker rm infostream-bahnapi
docker run -d -p 8101:8101 --name infostream-bahnapi infostream-bahnapi