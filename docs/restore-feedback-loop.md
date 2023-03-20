# Restore the pg dump

```
# download dump inside feedback-loop container and restore it
sudo docker exec --detach-keys='ctrl-@'  -it  feedback-loop_feedback-backend_1 bash

# Download feed-back-loop dump

wget "https://blsq-io.s3.eu-west-1.amazonaws.com/sanita-localhosting/feed-back-loop-production.dump.gz?response-content-__presigned_..._url" -O feed-back-loop-production.dump.gz

#if zipped, unzip it first
gzip -d feed-back-loop-production.dump.gz



# then restore
psql -U postgres -c 'create database feed_back_loop_production;'
psql -U postgres -h localhost -d feed_back_loop_production < feed-back-loop-production.dump


# delete the old files
rm feed-back-loop-production.dump
```

# Restore the logos and reports in minio

## Restore pdf reports

```
wget "https://blsq-io.s3.eu-west-1.amazonaws.com/sanita-localhosting/mailings.tar.gz?response-content-disposition=inline&..." -O  mailings.tar.gz

mkdir mailings
cd mailings
tar -xvzf ../mailings.tar.gz
```

assuming you installed mc

you can configure it to the server via mc alias

```
./mc alias set localhostminio https://minio.localhosting-mbtest.test.bluesquare.org <ACCESS_KEY_ID> <SECRET_KEY_ID>
```

then create the bucket with name feedback-loop-production:

you can check if the bucket is already exists by listing all buckets on the server:

```
./mc ls localhostminio
```

If it exists, It will appear in the list. Otherwise, you will have to create it with the command:

```
./mc mb localhostminio/feedback-loop-production
```

and restore the mailings folder

```
./mc cp --continue --recursive ./mailings/ localhostminio/feedback-loop-production/mailings
rm mailings.tar.gz
```

## Restore logos

```
wget "https://blsq-io.s3.eu-west-1.amazonaws.com/sanita-localhosting/logos.tar.gz?response-content-disposition=inline&..." -O  logos.tar.gz

mkdir logos
cd logos
tar -xvzf ../logos.tar.gz
```

and restore logos folder

```
./mc cp --continue --recursive ./logos/ localhostminio/feedback-loop-production/logos
rm logos.tar.gz
```
