#!/bin/bash

HOSTNAME=$(hostname -f)
DIR=/host-data/logs/web-static/$HOSTNAME
TAILFILE=$DIR/log.txt
mkdir -p $DIR

sed -ie "s@TAILFILE@$TAILFILE@g" /minifi/conf/flow.yml
sed -ie "s@HOSTNAME@$HOSTNAME@g" /minifi/conf/flow.yml

python /server.py 8000 $TAILFILE &
