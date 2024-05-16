# Update iaso 

## Make a database backup and store it somewhere

```
sudo ./toolbox iaso dump iaso_1
```

## Update inventory with new product image

To update the iaso version, retrieve the commit sha of recent [release](https://github.com/BLSQ/iaso/tags) which will be the iaso version.

Then update the inventory to put the new iaso version by replacing the value of `IASO_VERSION` by this commit sha.

```
 IASO_VERSION: "<new_iaso_version>"
```


## Launch ansible playbook

```
ansible-playbook -i <inventory_path> playbooks/blsq.yml
```

## Restart iaso and check the status

```
sudo systemctl restart iaso
sudo systemctl status iaso
```

## Run migrations and collectstatic

```
sudo docker exec --detach-keys='ctrl-@' -it iaso_iaso_1 bash
./manage.py migrate
./manage.py collectstatic
```

## Check the logs

```
journalctl -u iaso
```