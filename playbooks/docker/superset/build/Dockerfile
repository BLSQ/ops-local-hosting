FROM apache/superset
EXPOSE 8088

USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    
RUN pip install pymssql
RUN pip install psycopg2

COPY ./build/superset_config.py /app/superset_config.py

RUN chown superset /app/superset_config.py
RUN chmod 644 /app/superset_config.py


COPY ./build/entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh

USER superset

ENTRYPOINT ["/entrypoint.sh"]