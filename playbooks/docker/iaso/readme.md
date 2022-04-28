
# in iaso code base

## build a postgis image

```
cd docker/db
docker build . -t blsq/postgis:12
docker image push blsq/postgis:12
cd -
```

# build

```
docker build . -t blsq/iaso:latest
```