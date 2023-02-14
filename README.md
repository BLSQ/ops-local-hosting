# Procedure to setup a machine with "some bluesquare's products"

This assume you will provide one or multiple machines to host the products. These machine should be made available on the internet (eg so mobile application can submit their data to the server)

Avoid at all cost putting dhis2 on the same machine. Dhis2 is already a complex beast, adding these products there will just complexify your scaling up strategies.

Depending on the size of your organisation, you'll perhaps have to split products accross multiple machines.

The general target infrastructure will look like this

![image](https://user-images.githubusercontent.com/371692/218134323-3daeadd9-646d-4357-aeb1-e69db112e14e.png)

When we went for something like "systemd, docker images, docker-compose"

This allows some

- **homogeneity** to
  - stop/start
  - installation & versioning
  - consult the logs
- **isolation** (avoid package collisions)
  - Hesabu : ruby 3.2 + openssl 1.1
  - Enketo : nodejs
  - Iaso : python 3.7 + gdal + openssl 1.0
  - Dhis2 : java
- **easier relocation**
  - move to bigger machines
  - split products accross multiple machines
  - scale up ou disaster recovery (rebuild the infra)

## Setup a ansible on your laptop

clone this repository then

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
ansible-galaxy install -r requirements.yml
```

## Setup a machine

### if your organisation is more mature and use kubernetes

- stop here and call us

### in your cloud provider or in your hosting cabinet

- make the port 80 443 22 available to "the outside world"

### in aws light sails

```
aws-vault exec blsq --no-session
cd playbooks/aws-lightsail-instance/
ansible-playbook -e "instance_name=uganda state=present" create-delete-instance.yml
```

the output will look like

```
ok: [localhost] => {
    "address": "35.181.6.159"
}
```

this is the ip address of the new instance

![image](https://user-images.githubusercontent.com/371692/201858120-f7a7ca4c-17e8-4eef-ae5a-0bfbc5bcacbd.png)

you can check the domain is configured

```
dig localhosting-uganda.test.bluesquare.org
dig iaso.localhosting-uganda.test.bluesquare.org

localhosting-uganda.test.bluesquare.org. 275 IN A 35.181.6.159
```

if you plan to use such instance for a more "production" ready : attach a static ip !
or on the next restart the ip will change.

make sure the instance is available for https

![image](https://user-images.githubusercontent.com/371692/201864757-4d26fab7-619f-43f4-8941-34df123f191a.png)

## Configure inventory to connect to this machine

### Determine the case for https

- if you have an nginx upfront that will handle https certificates
  - `TLS_ENABLED: false`
- if you have the machine directly (ex lightsails)
  - `TLS_ENABLED: true`

### Determine the case for products to install

adapt the blsq_products_regexp depending

```
  blsq_products_regexp: .*(?:iaso|hesabu|dataviz).*
```

possible products : iaso, hesabu, dataviz, d2d

#### Create the inventory yml

```
all:
  children:
    iaso:
      hosts:
        ip1.ip2.ip3.ip4:
          ansible_ssh_private_key_file: ~/.ssh/myssh.pem
          ansible_user: ubuntu
          TRAEFIK_VERSION: "2.5.7"
          TRAEFIK_PWD: replaceme1
          TRAEFIK_USER: admin
          ACME_EMAIL: mdiop@bluesquarehub.com
          PORTAINER_PASSWORD: replacemewithhttpdpass
          DOMAIN_NAME: mysub.domain.com
          MINIO_ROOT_USER: minioroot
          MINIO_ROOT_PASSWORD: replace2
          ...
          D2D_...:
          ...
          HESABU_...
          ...
          IASO_...
          ENKETO_...
          ...
          DATAVIZ_...

```

replace each `replacemeX` with a different value you can use `uuidgen | tr -d - | tr -d '\n'`

generate a password based for PORTAINER_PASSWORD

```
docker run --rm httpd:2.4-alpine htpasswd -nbB admin '<<replaceme1>>' | cut -d ":" -f 2 | sed -r 's/[$]+/\$\$/g'
```

This calls htpasswd, keep only the password part and replace $ by $$ to get it right in docker-compose yml)
Note that if the portainer has already started, you need to stop it, delete the volume

- systemctl stop traefik
- docker volume ls
- docker volume rm traefik_portainer-data
- docker volume ls
- systemctl start traefik

### Configure ssh

```
Host localhosting-sms
  Hostname 35.181.6.159
  user ubuntu
  IdentityFile ~/.ssh/localhosting-eu-west-3.pem
  Port 22
```

save then test your access

```
 ssh localhosting-sms
```

### Launch ansible

go back to the root directory of ops-local-hosting and launch

```
ansible-playbook -i ./inventory/dev/ playbooks/iaso.yml
```

### Try to connect

Then test

http://iaso.localhosting-localhosting-sms.test.bluesquare.org/
https://minio-admin.localhosting-localhosting-sms.test.bluesquare.org/

It's not working ?

```
ssh localhosting-sms

systemctl status iaso
journalctl -u iaso

journalctl -u traefik
sudo systemctl restart traefik
journalctl -u traefik
```

## Restore dumps

If you were previously hosted on our SAAS offering, we'll need to coordinates upfront to provide you dumps with your data.

According to the product pick the right procedure

- some requires access to postgres dumps generated by our team,
- some requires extra files to upload in your minio instance

see these documents

- [iaso](./docs/restore-iaso.md)
- [hesabu](./docs/restore-hesabu.md)
- [dataviz](./docs/restore-dataviz.md)
- [d2d](./docs/restore-d2d.md)

## Setup backups

- setup a cron (pg_dump the databases)
- monitor daily these backups (success/failure, late,... )
- move these files for off site retention
- test the restore on seperate machine from time to time
