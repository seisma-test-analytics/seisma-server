#!/usr/bin/env bash

set -xe

API_PORT=${API_PORT:="5000"}
DOCS_PORT=${DOCS_PORT:="8080"}

PROCESSES=${PROCESSES:="4"}
GREENLETS=${GREENLETS:="100"}

DATABASE_URI=${DATABASE_HOST}:${DATABASE_PORT}

cat <<< "
[uwsgi]
no-orphans=1
module=seisma.wsgi:app
env=PYTHONPATH=/usr/local/src/seisma-api
master=1
processes=${PROCESSES}
gevent=${GREENLETS}
listen=100
log-5xx=1
logformat=%(ctime) %(method) %(uri) %(proto) %(user) %(addr) %(host) %(msecs) %(time) %(size) %(rss)
buffer-size=32768
harakiri=120
idle=3600
reload-mercy=10
need-app=1

gevent-monkey-patch
gevent-early-monkey-patch

ignore-sigpipe
ignore-write-errors
disable-write-exception
" > /etc/seisma.ini

while ! eval "curl ${DATABASE_URI}"; do
    echo "Waiting for database ready..."
    sleep 1
done

echo "Build docs"

sphinx-build -b html /usr/local/src/seisma-api/docs /usr/local/src/seisma-api/docs/_build

echo "Try to create or update database..."

set +e

python -m seisma db init
python -m seisma db migrate
python -m seisma db upgrade

set -e

echo "Run server..."

uwsgi --ini /etc/seisma.ini --socket 0.0.0.0:${API_PORT} --http-socket :${DOCS_PORT}
