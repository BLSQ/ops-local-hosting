FROM python:3.8

RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update && apt-get install -y postgresql-client-13 mariadb-client

RUN pip3 install pg_activity psycopg2-binary pgcli docker
RUN wget https://github.com/rbspy/rbspy/releases/download/v0.8.1/rbspy-x86_64-unknown-linux-gnu.tar.gz && tar xvzf rbspy-x86_64-unknown-linux-gnu.tar.gz && rm rbspy-x86_64-unknown-linux-gnu.tar.gz && mv ./rbspy-x86_64-unknown-linux-gnu /usr/bin/rbspy && chmod u+x /usr/bin/rbspy
ADD lhc lhc

ENTRYPOINT ["./lhc"]