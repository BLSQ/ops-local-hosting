# Restore the pg dump

```
# download dump inside feedback-loop-db container and restore it
sudo docker exec --detach-keys='ctrl-@' -it feedback-loop_db_1 bash

# Download feed-back-loop dump

wget "https://blsq-io.s3.eu-west-1.amazonaws.com/sanita-localhosting/feed-back-loop-production.dump.gz?response-content-__presigned_..._url" -O feed-back-loop-production.dump.gz

#if zipped, unzip it first
gzip -d feed-back-loop-production.dump.gz


# Check the DATABASE_URL from feedback-loop_backend container
sudo docker exec --detach-keys='ctrl-@'  -it feedback-loop_feedback-backend_1 bash
env

# then restore
sudo docker exec --detach-keys='ctrl-@'  -it feedback-loop_db_1 bash
export DATABASE_URL=
pg_restore --format=c --verbose --no-acl --clean --jobs=6 --no-owner -d feed_back_loop_production  feed-back-loop-production.dump


# delete the old files
rm feed-back-loop-production.dump
```

# Restore the logos and reports in minio

## Restore pdf reports

assuming you installed mc

you can configure it to the server via mc alias

```
mc alias set localhostminio $ENDPOINT $ACCESS_KEY_ID $SECRET_ACCESS_KEY
mc admin info localhostminio
mc ls localhostminio
```
get a presigned url from our blsq s3 bucket

download the mailings folder on the host inside feedback-backend container and restore it

```
sudo docker exec --detach-keys='ctrl-@'  -it feedback-loop_feedback-backend_1  bash
wget "https://blsq-io.s3.eu-west-1.amazonaws.com/sanita-localhosting/mailings.tar.gz?response-content-disposition=inline&..." -O  mailings.tar.gz
mkdir mailings
cd mailings
tar -xvzf ../mailings.tar.gz
mc cp --continue --recursive ./mailings/ localhostminio/feedback-loop/mailings
rm mailings.tar.gz
```

## Restore logos

```
wget "https://blsq-io.s3.eu-west-1.amazonaws.com/sanita-localhosting/logos.tar.gz?response-content-disposition=inline&..." -O  logos.tar.gz
mkdir logos
cd logos
tar -xvzf ../logos.tar.gz
mc cp --continue --recursive ./logos/ localhostminio/feedback-loop/logos
rm logos.tar.gz
```
