[uwsgi]
no-orphans=1
module=seisma.wsgi:app
env=SEISMA_SETTINGS={{ config }}
env=PYTHONPATH={{ pythonpath }}
master=1
logfile-chmod=644
processes={{ processes }}
gevent=100
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
