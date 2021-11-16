
```
git clone git@github.com:BLSQ/orbf2.git
cd orbf2
docker build -t blsq/orbf2 .
docker push blsq/orbf2:latest
```


### TOOLBOX docker

export DATABASE_URL=$(docker exec docker_hesabu-web_1 bash -c 'echo "$DATABASE_URL"')
docker run -it --rm  --network=hesabu_default -e DATABASE_URL=${DATABASE_URL} blsq/toolbox

```
DATABASE_URL= $(docker exec hesabu_hesabu-web_1 bash -c 'echo "$DATABASE_URL"')
docker run -it --rm  --network=hesabu_default -e DATABASE_URL=$DATABASE_URL blsq/toolbox
sudo docker run -it --rm  --network=hesabu_default -e PGPASSWORD=passwordpostgres blsq/toolbox pgcli -h hesabu-db -U scorpio -d scorpio_production -p 5432
```

Dockerfile 

docker build -t blsq/toolbox .

