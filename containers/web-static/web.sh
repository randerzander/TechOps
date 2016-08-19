#!/bin/bash

HOSTNAME=$(hostname -f)
DIR=/host-data/logs/web/$HOSTNAME
TAILFILE=$DIR/web.log
mkdir -p $DIR

sed -ie "s@TAILFILE@$TAILFILE@g" /minifi/conf/flow.yml

python /server.py 8000 $TAILFILE &
