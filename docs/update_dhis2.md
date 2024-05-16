# Update DHIS2 

We recommend to set up a test environment, follow [migration](https://github.com/dhis2/dhis2-releases/tree/master/releases) procedures, restore backup of production, then update the test environment with the dhis2 version that you want.

If everything is fine, then replay update on production environment.

# Procedures

## Make a database backup and store it somewhere

```
sudo ./toolbox dhis2 dump dhis2
```

## Update inventory with new product image

We release docker images of dhis2 versions https://hub.docker.com/r/blsq/dhis2/tags.

Update inventory with the new dhis2 version that you want.

```
 DHIS2_VERSION: "<dhis2_version>"
```
**NB**: Check https://github.com/BLSQ/ops-dhis2-images for other [variables](https://github.com/BLSQ/ops-dhis2-images/blob/main/templates/dhis.conf.tmpl) to add to the inventory if necessary.

## Launch ansible playbook

```
ansible-playbook -i <inventory_path> playbooks/blsq.yml
```

## Restart iaso and check the status

```
sudo systemctl restart dhis2
sudo systemctl status dhis2
```

## Check the logs

```
journalctl -u dhis2
```