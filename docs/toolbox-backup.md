# Setup backups with toolbox

## Install the ops-local-hosting-toolbox

Install the [toolbox](https://github.com/BLSQ/ops-local-hosting-toolbox) script on the host where the docker containers are running.

```
curl https://raw.githubusercontent.com/BLSQ/ops-local-hosting-toolbox/main/run -o toolbox
chmod u+x toolbox
```

## Trigger dumps
 
You can manually trigger dumps which will be stored in `/home/backups`.

```
sudo ./toolbox dataviz dump dataviz-worker
sudo ./toolbox hesabu dump hesabu-worker
sudo ./toolbox d2d dump d2d-backend-sidekiq
sudo ./toolbox iaso dump iaso_1
```

## Connect to postgres DB
```
sudo ./toolbox iaso cli iaso_1
```

## Make a diagnose

The json file is stored in `/home/backups`.
```
sudo ./toolbox iaso diagnose cli iaso_1
```

## Trigger postgres backups as a cron 

Edit crontab file
```
crontab -e 
```
Add line containing cron expression 
```
0 0 * * *  sudo ./toolbox dataviz dump dataviz-worker >/dev/null 2>&1
0 1 * * *  sudo ./toolbox hesabu dump hesabu-worker >/dev/null 2>&1
0 2 * * *  sudo ./toolbox iaso dump iaso_1 >/dev/null 2>&1

```

## Delete old postgres backups and keep the 7 most recent files as cron 

Download the cleanup_backups script 
```
curl https://raw.githubusercontent.com/BLSQ/ops-local-hosting-toolbox/main/cleanup_backups -o cleanup_backups
chmod u+x cleanup_backups
```

Edit crontab file
```
crontab -e 
```

Schedule the script with cron
```
0 8 * * * sudo ./cleanup_backups
```
