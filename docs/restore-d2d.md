# restore the db dump

```
# download dump inside d2d container and restore it
sudo docker exec --detach-keys='ctrl-@'  -it  d2d_d2d-backend_1 bash

# Download d2d dump
wget "https://blsq-share.s3.eu-west-3.amazonaws.com/uganda-localhosting/d2d.tenant-64.dump.gz??response-c__presigned_..._url" -O d2d.dump.gz

#if zipped, unzip it first
gzip -d d2d.dump.gz

# then restore
pg_restore --format=c --verbose --no-acl --clean --jobs=6 --no-owner -d $DATABASE_URL d2d.dump

# delete the old files
rm d2d.dump

```
