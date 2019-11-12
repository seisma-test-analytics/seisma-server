FROM python:3.5

RUN apt-get update -qqy && apt-get install -y gcc make
RUN apt-get install -y libreadline-gplv2-dev libncursesw5-dev \
    libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

ENV PYTHONPATH=/usr/local/src/seisma-server

COPY . /usr/local/src/seisma-server
WORKDIR /usr/local/src/seisma-server

RUN pip install -r requirements.txt -U

ENTRYPOINT ["/usr/local/src/seisma-server/docker-entrypoint.sh"]
