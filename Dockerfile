FROM python:3.11.1-slim-bullseye

ARG VERSION=0.1.7

RUN useradd -ms /bin/bash dans

USER dans
WORKDIR /home/dans

ENV PYTHONPATH=/home/dans/dans-ldn-inbox-service/src
ENV BASE_DIR=/home/dans/dans-ldn-inbox-service
ENV DB_DIR=/home/dans/dans-ldn-inbox-service/data/db
#RUN mkdir -p ${BASE_DIR}


COPY ./dist/*.* .

#
RUN mkdir -p ${BASE_DIR} && \
    pip install --no-cache-dir *.whl && rm -rf *.whl && \
    tar xf dans_ldn_inbox_service-${VERSION}.tar.gz -C ${BASE_DIR} --strip-components 1

#COPY src/conf/.secrets.toml ${BASE_DIR}/src/conf/.secrets.toml

WORKDIR ${BASE_DIR}
CMD ["python", "src/main.py"]
#CMD ["tail", "-f", "/dev/null"]
