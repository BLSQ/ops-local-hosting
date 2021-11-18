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

You can configure your ~/.ssh/config to connect easily

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

## Set up POSTGRESQL

From the server, you will run the follow command to install and configure postgresql.

```
ansible-playbook -i <INVENTORY> playbooks/docker/dhis2/postgres/postgresql.yml 
```

## Restore DB

Then we will provide you with a presigned S3 URL to upload the dump.

And you can follow these steps to restore the dump.

```
ssh dhis2-server
sudo su - postgres
curl 'S3_URL' -o <BUCKET_NAME>.dump.gz
unzip <BUCKET_NAME>.dump.gz

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
      --dbname="<dhis_db_name>" \
      <BUCKET_NAME>.dump.gz
```

## Set up DHIS2

From the server, you will run the follow command to install DHIS2.

```
ansible-playbook -i <INVENTORY> playbooks/dhis2.yml
```

Checking the status and logs

```
systemctl status dhis2 
journalctl -u dhis2
```

## Restore in local dhis2 data from s3

## Inventory template 

You must provide a file to store your inventory.

In this inventory, provide values of all environment variables defined into `.env` file.

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
          TRAEFIK_VERSION: <v2.4>
          dhis_db_user: <dhis2>
          dhis_db_password: <XXXXXX>
          dhis_db_name: <dhis2_db>
          config_system_locale: <en_US.UTF-8>
        
    ungrouped: {}
```