# minio debug/testing

```
sudo docker exec --detach-keys='ctrl-@'  -it  iaso_iaso_1 bash
```

install mc command line

```
curl https://dl.min.io/client/mc/release/linux-amd64/mc \
  --create-dirs \
  -o $HOME/minio-binaries/mc

chmod +x $HOME/minio-binaries/mc
export PATH=$PATH:$HOME/minio-binaries/
```

assuming you have installed mc binaries

```
mc alias set localhostminio $AWS_S3_ENDPOINT_URL $AWS_ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY
mc admin info localhostminio
mc ls localhostminio

mc policy set download localhostminio/iaso-prod
mc anonymous set download localhostminio/iaso-prod/iasostatics/
mc anonymous set public localhostminio/iaso-prod/iasostatics/
```

# Restore with existing data

## Restore db from dump

get a presigned url from our blsq s3 bucket

download it on the host inside iaso container and restore it

```
sudo docker exec --detach-keys='ctrl-@'  -it  iaso_iaso_1 bash
wget "https://bls.s3.eu-west-1.amazonaws.com/burundi/iaso.tenant-13.dump.gz?response-content-disposition=inline&X-Amz-Security-Token=<<theverylongtoken>>" -O iaso.tenant-13.dump.gz

#if zipped, unzip it first
unzip iaso.tenant-13.dump.gz
# then restore
pg_restore --format=c --verbose --no-acl --clean --jobs=6 --no-owner -d $DATABASE_URL  iaso.tenant-13.dump
# delete the old files
rm iaso.tenant-13.dump
rm iaso.tenant-13.dump.gz

```

## restoring s3

download the zip of iaso files, unzip

```
wget "https://blspresigned_kilometric_url" -O burundi-iaso-s3.tar.gz

mkdir x && cd x
tar -xzvf ../burundi-iaso-s3.tar.gz
```

assuming you installed mc and configured it (cfr mc alias)

```
mc cp --continue --recursive ./instances/ localhostminio/iaso-prod/instances
mc cp --continue --recursive ./forms/ localhostminio/iaso-prod/forms
mc cp --continue --recursive ./instancefiles/ localhostminio/iaso-prod/instancefiles
```
# Setup Iaso with empty data

- Connect to iaso container

```
sudo docker exec --detach-keys='ctrl-@'  -it  iaso_iaso_1 bash
```

- Install mc command line

```
curl https://dl.min.io/client/mc/release/linux-amd64/mc \
  --create-dirs \
  -o $HOME/minio-binaries/mc

chmod +x $HOME/minio-binaries/mc
export PATH=$PATH:$HOME/minio-binaries/
```

- Set permissions for public access to iaso-prod/iasostatics

```
mc alias set localhostminio $AWS_S3_ENDPOINT_URL $AWS_ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY
mc admin info localhostminio
mc ls localhostminio

mc policy set download localhostminio/iaso-prod
mc anonymous set download localhostminio/iaso-prod/iasostatics/
mc anonymous set public localhostminio/iaso-prod/iasostatics/
```
- Download JS assets

```
./manage.py collectstatic
```

- Create a superuser

To log in to the api or the Django admin, a superuser needs to be created with:

```
./manage.py createsuperuser
```

- Log in to iaso interface with the superuser account 

Now create the first user and define the necessary modules

 https://iaso.<domain_name>/dashboard/setupAccount

- Then use this user's credentials to log into the IASO interface

https://iaso.<domain_name>/login
