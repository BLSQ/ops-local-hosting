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
