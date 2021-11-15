#!/bin/bash
docker-compose -f docker-compose-minio.yml -f docker-compose-hesabu.yml up

docker inspect -f 'hesabu : {{range.NetworkSettings.Networks}}http://{{.IPAddress}}:3000 | {{end}}' docker_hesabu-web_1
docker inspect -f 'minio : {{range.NetworkSettings.Networks}}http://{{.IPAddress}}:3000 | {{end}}' docker_minio_1