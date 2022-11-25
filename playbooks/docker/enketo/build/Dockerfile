FROM enketo/enketo-express:4.1.0

EXPOSE 3000

#ADD config.json /srv/src/enketo_express/config/config.json
ADD ./build/create_config.py /srv/src/enketo_express/setup/docker/create_config.py

CMD ["/bin/bash", "-c", "${ENKETO_SRC_DIR}/setup/docker/start.sh"]
