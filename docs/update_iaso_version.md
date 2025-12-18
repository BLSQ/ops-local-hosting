# Update iaso 

## Make a database backup and store it somewhere

```
sudo ./toolbox iaso dump iaso_1
```

## Update inventory with new product image

To update the iaso version, retrieve the commit sha of recent [release](https://github.com/BLSQ/iaso/releases) which will be the iaso version.

Then update the inventory to put the new iaso version by replacing the value of `IASO_VERSION` by this commit sha.

```
 IASO_VERSION: "<new_iaso_version>"
```


## Launch ansible playbook

```
cd ops-local-hosting
source env/bin/activate
ansible-playbook -i <inventory_path> playbooks/blsq.yml
```

## Check the iaso status and logs

```
sudo systemctl status iaso
journalctl -u iaso
```

## Run migrations and collectstatic

After the upgrade, if you don't encounter an error, simply run:
```
# Run the migrations again
./manage.py migrate

# Run collectstatic
./manage.py collectstatic

# Exit the container
exit
```

But, you may encounter the following migration error: 

`Migration audit.0006_modification_org_unit_change_request is applied before its dependency iaso.0343_importgpkg_default_valid on database default`.

To fix the issue, follow these steps:

```
# Connect to iaso worker container
sudo docker exec --detach-keys='ctrl-@' -it iaso-iaso-worker-1 bash

# Temporarily rename the squashed migration file
mv  iaso/migrations/0001_squashed_0343_importgpkg_default_valid.py iaso/migrations/0001_squashed_0343_importgpkg_default_valid.txt

# Edit the migration causing the issue
# Replace `0001_squashed_0343_importgpkg_default_valid` with `0236_auto_20231012_0955`
nano hat/audit/migrations/0006_modification_org_unit_change_request.py

# Run the migrations
./manage.py migrate

# Restore the original squashed migration file
mv  iaso/migrations/0001_squashed_0343_importgpkg_default_valid.txt iaso/migrations/0001_squashed_0343_importgpkg_default_valid.py

# Edit the migration again
# Replace `0236_auto_20231012_0955` back with `0001_squashed_0343_importgpkg_default_valid` 
nano hat/audit/migrations/0006_modification_org_unit_change_request.py

# Run the migrations again
./manage.py migrate

# Run collectstatic
./manage.py collectstatic

# Exit the container
exit
```

## Restart iaso and check the status

```
sudo systemctl restart iaso
sudo systemctl status iaso
```

## Check the logs

```
journalctl -u iaso
```
