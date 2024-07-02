# ops-local-hosting

## Local setup

### Create a venv in the directory

```
python3 -m venv env
```

### Install the dependencies (ansible and external ansible playbooks)

```
source env/bin/activate
pip install -r requirements.txt
ansible-galaxy install -r requirements.yml
```

## Connect to server

You can configure your ~/.ssh/config to connect easily.

```
Host dhis2-server
  Hostname <IP_ADDRESS>
  user <USERNAME>
  IdentityFile <PEM_FILE>
  Port 22

```

Connect to the server using: 

```
ssh dhis2-server
```
## Inventory template 

You need to provide a file to store your inventory.

Specify the values of the mandatory environment variables defined in the [dhis2.env](https://github.com/BLSQ/ops-local-hosting/blob/main/playbooks/docker/dhis2.env) file.

Here is an example of template:

```
all:
  children:
    dhis2:
      hosts:
        <IP_ADDRESS>:
          TRAEFIK_PWD: <TRAEFIK_PWD>
          TRAEFIK_USER: <TRAEFIK_PWD>
          ansible_ssh_private_key_file: <PEM_FILE>
          ansible_user: <USERNAME>
          DOMAIN_NAME: <URL>
          ACME_EMAIL: <EMAIL>
          DHIS2_DATABASE_USER: <dhis2_user>
          DHIS2_DATABASE_PASSWORD: <dhis2_password>
          DHIS2_DATABASE_NAME: <dhis2_db_name>
          DHIS2_DATABASE_HOST: <database_hostname>
          DHIS2_POSTGRES_VERSION: <dhis2_postgres_version>
          DHIS2_DOMAIN_NAME: <dhis2_url>
          DHIS2_VERSION: "2.37.9"
          config_system_locale: <en_US.UTF-8>
          TLS_ENABLED: true
          blsq_products_regexp: .*(?:dhis2).*
        
    ungrouped: {}
``` 
## Set up DHIS2 with Postgresql

Run the following command to install and configure Postgresql on the host and deploy DHIS2 with docker.

```
ansible-playbook -i <INVENTORY> playbooks/blsq.yml
```

Checking the status and logs

```
systemctl status dhis2 
systemctl status traefik 

journalctl -u dhis2
journalctl -u traefik

```

## Restore DHIS2 DB

Then we will provide you with a presigned S3 URL to upload the dump.

As the database is on the host, follow these steps to download the dump.

```
ssh dhis2-server
sudo su - postgres
wget 'S3_presigned_url' -O dhis2-db.dump.gz
gzip -d dhis2-db.dump.gz

```

Then you can restore the dump by running:

```
pg_restore \
      --format=c \
      --verbose \
      --no-acl \
      --clean \
      --jobs=6 \
      --no-owner \
      --dbname="<dhis2_db_name>" \
      dhis2-db.dump
```

## Restore DHIS2 files from s3

We will provide you with a presigned S3 URL to upload the zipped folder.

Download it on the host inside dhis2 container and restore it.

```
# download dump
docker exec -it dhis2_dhis2_1 bash 
wget "S3_presigned_url" -O dhis2-files.tar.gz 

# unzip it
tar -xvzf dhis2-files.tar.gz 

# then restore
mv dhis2-files/apps/ files/
mv dhis2-files/dataValue/ files/
```


