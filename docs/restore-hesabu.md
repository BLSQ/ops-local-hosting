# Restore the db dump

```
# download dump inside hesabu container and restore it
sudo docker exec --detach-keys='ctrl-@'  -it  hesabu_hesabu-web_1 bash

# Download hesabu dump
wget "https://blsq.s3.eu-west-1.amazonaws.com/uganda-localhosting/hesabu-project-110-30-01-23_09-50.tar.gz?response-c__presigned_..._url" -O hesabu.tar.gz

#if zipped, unzip it first
gzip -d  hesabu.tar.gz

# create tables
rake db:setup

# then restore
psql $DATABASE_URL -f  hesabu.tar

# delete the old files
rm hesabu.tar

```

# Restore a latest db dump

```
# download dump inside hesabu container and restore it
sudo docker exec --detach-keys='ctrl-@'  -it  hesabu_hesabu-web_1 bash

# Connect to db and terminate all active connections 
psql $DATABASE_URL -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'orbf2' AND pid <> pg_backend_pid();"

# Drop the database
DISABLE_DATABASE_ENVIRONMENT_CHECK=1 rake db:drop

# Download the latest hesabu dump
wget "https://blsq.s3.eu-west-1.amazonaws.com/uganda-localhosting/hesabu-project-110-03-07-24_09-50.tar.gz?response-c__presigned_..._url" -O hesabu.tar.gz

#if zipped, unzip it first
gzip -d  hesabu.tar.gz

# create tables
rake db:setup

# then restore
psql $DATABASE_URL -f hesabu.tar

# delete the old files
rm hesabu.tar

```
