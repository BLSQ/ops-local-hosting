# Restore with existing data

## Restore the pg dump

Start a bash in the context of dataviz backend

```
cd /srv/docker/dataviz/
docker-compose ps
journalctl -u dataviz
docker-compose run dataviz-backend bash
```

Then download the pg dump and restore it

```
wget "https://bls.s3.eu-west-1.amazonaws.com/uganda-localhosting/dataviz.dump?presigne...durl" -O dataviz.dump

pg_restore --format=c --verbose --no-acl --clean --jobs=6 --no-owner -d $DATABASE_URL dataviz.dump
```

After that you might need to adapt a bit the url of domain

```
bundle exec rails c

# check the project info matches
Project.first

# adapt the project domain and cache interval

Project.first.update(
    domain:"dataviz.health.go.ug",
    cache_interval: 1
    )
```

Once the dataviz starts looking okish (some branding showed, perhaps not all the data) you can trigger the process to populate the cache from dhis2

```
bundle exec rake cache_warmup:run
```

## Restore the logos and publications in minio

Assuming you have mc binary and alias configured
and received a presigned url

```
wget "https://bls.s3.eu-west-1.amazonaws.com/-localhosting/dataviz-logos-bf8bcaa7-7adf-4a07-ae3d-b6163e929971.tar.gz?response-content-disposition=inline&..." -O dataviz-logos.tar.gz
mkdir dataviz
cd dataviz
tar -xvzf ../dataviz-logos.tar.gz
cd tmp/
cd bf8bcaa7-7adf-4a07-ae3d-b6163e929971/
mc cp --continue --recursive ./uploads/ localhostminio/dataviz/production/uploads
wget "https://geojson-countries.s3.eu-west-1.amazonaws.com/<country>.geo.json"
mc cp --continue bfa.geo.json localhostminio/geojson-countries/<country>.geo.json
rm <country>.geo.json
rm dataviz-logos.tar.gz
```

# Restore with empty data

## Restore the pg dump with schema and migrations only

Start a bash in the context of dataviz backend

```
cd /srv/docker/dataviz/
docker-compose ps
docker-compose run dataviz-backend bash
```

Then download the pg dump with schema only and restore it

```
wget "https://bls.s3.eu-west-1.amazonaws.com/localhosting/dataviz-empty.dump?presigne...durl" -O dataviz-empty.dump

pg_restore --verbose --clean --no-acl --no-owner -d $DATABASE_URL dataviz-empty.dump
```

After that download the pg dump with migrations and restore it


```
wget "https://bls.s3.eu-west-1.amazonaws.com/localhosting/dataviz-migrations.dump?presigne...durl" -O dataviz-migrations.dump

pg_restore --verbose --no-acl --no-owner -d $DATABASE_URL dataviz-migrations.dump
```


## Add the geojson file of country in minio

Assuming you have mc binary and alias configured
and received a presigned url

```
wget "https://geojson-countries.s3.eu-west-1.amazonaws.com/<country>.geo.json"
mc cp --continue bfa.geo.json localhostminio/geojson-countries/<country>.geo.json
rm <country>.geo.json
```