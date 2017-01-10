#!/bin/bash

PATH=$PATH:/usr/local/bin:/usr/local
export PATH

True=1
False=0

UWSGI_BIN=`which uwsgi`

PID_FILE="/var/run/seisma.pid"
LOG_FILE="/var/log/seisma.log"
SOCKET_FILE="/var/run/seisma.sock"
CONFIG_FILE="/etc/seisma.ini"


function is_running() {
    if [ -f "$PID_FILE" ]; then
        exist=`ps -ef | grep -v grep | grep $PID_FILE | awk '{print $2}'`

        if [ "$exist" ]; then
            return $True
        else
            rm $PID_FILE
        fi

    fi

    return $False
}

function status() {
    echo "==== Seisma status ===="

    if [ $( is_running ) $? -eq $True ]; then
        echo
        echo "Seisma is running"

    else
        echo
        echo "Seisma is stopped"
    fi
}

function start() {
    echo "==== Seisma start ===="

    if [ $( is_running ) $? -eq $True ]; then
        echo
        echo "Seisma already started"
        exit 0
    else
        touch $PID_FILE
        $UWSGI_BIN --ini "$CONFIG_FILE" --pidfile $PID_FILE --daemonize $LOG_FILE --socket $SOCKET_FILE
    fi
}

function stop() {
    echo "==== Seisma stop ===="

    if [ $( is_running ) $? -eq $True ]; then
        if [ -f "$PID_FILE" ]; then
            $UWSGI_BIN --stop $PID_FILE
            rm $PID_FILE
        fi

        echo "Done."
    else
        echo "Seisma already stopped?"
        exit 0
    fi
}


case "$1" in
    'start')
            start
            ;;
    'stop')
            stop
            ;;
    'restart')
            stop
            echo "Sleeping..."; sleep 1 ;
            start
            ;;
    'status')
            status
            ;;
    *)
            echo
            echo "Usage: $0 { start | stop | restart | status }"
            echo
            exit 1
            ;;
esac


exit 0