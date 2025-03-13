# Upgrade iaso db to postgres 16


## Make a db backup with postgres 12

Connect to the server and take a dump of the current db (12) using toolbox

```
sudo ./toolbox iaso dump iaso_1
```

## Add a new container with postgres 16

- Go to the Iaso configuration directory
```
cd /srv/docker/iaso/
```

- Edit the docker-compose.yml file to add a new db container with postgres 16
```
sudo nano /srv/docker/iaso/docker-compose.yml
```
```
version: "3.3"
services:
  db:
    image: blsq/postgis:12
    ports:
      - "5433:5432"
    volumes:
      - ./storage/db:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: ${IASO_DB_NAME}
      POSTGRES_USER: ${IASO_DB_USER}
      POSTGRES_PASSWORD: ${IASO_DB_PASSWORD}
  db-16:
    image: blsq/postgis:16
    ports:
      - "5434:5432"
    volumes:
      - ./storage/db-16:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: ${IASO_DB_NAME}
      POSTGRES_USER: ${IASO_DB_USER}
      POSTGRES_PASSWORD: ${IASO_DB_PASSWORD}
```

## Launch docker compose

- Restart iaso service
```
sudo systemctl restart iaso
```
- Check the list of iaso containers
```
sudo docker compose ps
```
## Restore postgres 12 dump in the db container 16

- Copy the dump into the iaso container
```
sudo docker cp /home/backups/iaso_iaso_1-2025-01-09_13h16.dump iaso_iaso_1:/opt/app
```

- Connect to iaso container
```
sudo docker exec --detach-keys='ctrl-@'  -it  iaso_iaso_1 bash
```
- Restore the dump
```
export DB_16=postgres://userpost:<password>@db-16/iaso
pg_restore --format=c --verbose --no-acl --clean --jobs=6 --no-owner -d $DB_16  iaso_iaso_1-2025-01-09_13h16.dump 
exit
```

## Archive db 12 volume and Rename db 16 volume

- Zip db 12 volume
```
cd /srv/docker/iaso/storage
sudo tar -czvf db-12.tar.gz db/
```
- Rename db 16 volume
```
cd /srv/docker/iaso/storage
sudo mv db db-12
sudo mv db-16/ db
``` 
## Edit the docker-compose.yml file to remove the container with postgres 12 and keep the 16 

- Stop service
```
sudo systemctl stop iaso
```
- Edit the docker-compose.yml file to remove the container `db-16`  and keep the container `db` by just changing postgis image
```
sudo nano /srv/docker/iaso/docker-compose.yml
```
```
version: "3.3"
services:
  db:
    image: blsq/postgis:16
    ports:
      - "5433:5432"
    volumes:
      - ./storage/db:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: ${IASO_DB_NAME}
      POSTGRES_USER: ${IASO_DB_USER}
      POSTGRES_PASSWORD: ${IASO_DB_PASSWORD}
```

## Launch docker compose

- Restart iaso service
```
sudo systemctl restart iaso
```
- Check the list of iaso containers
```
sudo docker compose ps
```
- Check the logs 

```
journalctl -u iaso
```

## Update iaso docker compose file in ops-local-hosting directory

- Go the ops-local-hosting repo where you launch the ansible playbook

```
cd ops-local-hosting
```
- Edit the docker-compose.yml file by changing the postgis image tag to 16

```
sudo nano playbooks/docker/iaso/docker-compose.yml
```
```
version: "3.3"
services:
  db:
    image: blsq/postgis:16
    ports:
      - "5433:5432"
    volumes:
      - ./storage/db:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: ${IASO_DB_NAME}
      POSTGRES_USER: ${IASO_DB_USER}
      POSTGRES_PASSWORD: ${IASO_DB_PASSWORD}
```
- Launch the ansible playbook

```
cd ops-local-hosting
source env/bin/activate
ansible-playbook -i <inventory_path>> playbooks/blsq.yml
```
