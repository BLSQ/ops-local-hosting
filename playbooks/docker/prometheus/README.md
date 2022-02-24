# Prometheus

DHIS2 can export Prometheus compatible metrics for monitoring DHIS2 nodes.

## Setup Prometheus 

### Define the inventory
```
all:
  children:
    prometheus:
      hosts:
        3.125.17.107:
          TRAEFIK_PWD: XXXX
          TRAEFIK_USER: ttt
          ansible_ssh_private_key_file: ~/.ssh/prometheus-eu-central-1.pem
          ansible_user: ubuntu
          DOMAIN_NAME: prometheus.bluesquare.org 
          ACME_EMAIL: mdiop@bluesquarehub.com
          config_system_locale: en_US.UTF-8
          PROMETHEUS_TAG: v2.32.1
          ADMIN_PASSWORD: XXXXXXXX
          MONITORING_TOKEN: XXXXXXXXXXX
          SECRET_KEY_BASE: XXXXXXXXXXXXXXXX
          MINIO_ROOT_USER: miniouser
          MINIO_ROOT_PASSWORD: XXXXXXX
          TRAEFIK_VERSION: v2.4
          POSTGRES_VERSION: 13
          REDIS_VERSION: 6.2.5
        
    ungrouped: {}
```
### Configure Prometheus to pull metrics from DHIS2 instances

We need to edit a configuration file named `prometheus.yml`. 

Prometheus configuration file is divided into three parts: 
- `global`: we can find the general configuration of Prometheus: `scrape_interval` defines how often Prometheus scrapes targets, `evaluation_interval` controls how often the software will evaluate rules.
- `rule_files`: which contains information of the location of any rules we want the Prometheus server to load.
- `scrape_configs`: which contains the information which resources Prometheus monitors.


DHIS2 Sandbox Prometheus monitoring file looks like this example:

```
global:
  scrape_interval: 15s
  external_labels:
    monitor: 'prometheus'

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
  - job_name: dhis2
    metrics_path: /api/metrics
    scheme: https
    static_configs:
      - targets: ['sandbox.bluesquare.org']
    basic_auth:
      username: admin
      password: XXXXXXXXXXXXX
```

In the `scrape_configs` part we have defined the DHIS2 sanbbox instance. The `basic_auth` blocks contains the credentials required to access the metrics API.

The `targets` block contains the URL of DHIS2 instance.

### Basic authentication

If we want to require a username and password from all users accessing the Prometheus instance:
- Generate a hashed password using htpasswd like this:

`echo $(htpasswd -nbB <USER> "<PASS>")`

Save that password somewhere, we will use it in the next step.

- Modifying the web configuration file name `web.yml`

Edit the web.yml file by replacing the `<USER>` and `<HASHED_PASS>` which has just been generated.
```
basic_auth_users:
    <USER> : <HASHED_PASS>
```
We can add multiple users to the file.

### Run Prometheus

Let's execute the following command to deploy the prometheus instance:

```
ansible-playbook -i <INVENTORY> playbooks/prometheus.yml 
```

To begin, access to https://prometheus.bluesquare.org and enter the username and password that we defined with htpassword.



## DHIS2 Configuration

The monitoring subsystem is disabled by default in DHIS2.

To configure DHIS2 to export one or more metrics, it must be activated by defining a set of properties in the `templates/dhis.conf.tmpl` file of the `dhis2-docker-eb` repository for each DHIS2 instance.

The metrics can be enabled by setting to `on` the following configuration keys (the default is `off`):

| key name                       | value     | metrics              |
|--------------------------------|-----------|----------------------|
| `monitoring.api.enabled`       | off \| on | API                  |
| `monitoring.jvm.enabled `      | off \| on | JVM                  |
| `monitoring.dbpool.enabled`    | off \| on | Connection Pool      |
| `monitoring.hibernate.enabled` | off \| on | Hibernate            |
| `monitoring.uptime.enabled`    | off \| on | Uptime               |
| `monitoring.cpu.enabled`       | off \| on | CPU                  |


## DHIS2 metrics

DHIS2 exposes a series of metrics which can be scraped by Prometheus. Currently, the metrics exposed by the application are:

- DHIS2 API (response time, number of calls, etc.)
- JVM (Heap size, Garbage collection, etc.)
- Hibernate (Queries, cache, etc)
- C3P0 Database pool
- Application uptime
- CPU