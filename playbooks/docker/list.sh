#!/bin/bash
docker inspect -f 'hesabu : {{range.NetworkSettings.Networks}}http://{{.IPAddress}}:3000 | {{end}}' docker_hesabu-web_1
docker inspect -f 'minio  : {{range.NetworkSettings.Networks}}http://{{.IPAddress}}:9000 | {{end}}' docker_minio_1