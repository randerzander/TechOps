#!/bin/bash

HOSTNAME=$(hostname -f)
DIR=/host-data/logs/zeppelin/$HOSTNAME
TAILFILE=$DIR/zeppelin--$HOSTNAME.log
mkdir -p $DIR
touch $TAILFILE

sed -ie "s@TAILFILE@$TAILFILE@g" /minifi/conf/flow.yml
sh /zeppelin/bin/zeppelin-daemon.sh start
sleep 5
tail -f /zeppelin/logs/zeppelin--$HOSTNAME.log
