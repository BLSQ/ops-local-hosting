#!/bin/bash
set -e

function admin_is_not_created() {
  superset fab list-users 2>/dev/null | grep -vq "role:\[Admin\]"
}

export SUPERSET_CONFIG_PATH=/app/superset_config.py

admin_is_not_created &&
  superset fab create-admin --username admin --firstname Superset \
    --lastname Admin --email admin@example.com --password "${ADMIN_PASSWORD}"

superset db upgrade
superset init

/usr/bin/run-server.sh "\$@"