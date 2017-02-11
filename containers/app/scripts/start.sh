#!/bin/bash
set -eu

BASHRC_FILE=/root/.bashrc
rm $BASHRC_FILE
echo "export MASTER_FQDN=monitor.dev" >> $BASHRC_FILE
echo "export HOSTNAME=$(hostname -f)" >> $BASHRC_FILE
echo "export IP=$(hostname -i)" >> $BASHRC_FILE
echo "export MINIFI_HOME=/minifi" >> $BASHRC_FILE
echo "export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk" >> $BASHRC_FILE
source $BASHRC_FILE

# Setup and start NiFi
PROTO_PORT=1025
SOCKET_PORT=1026

# Give master.dev a chance to start NiFi
sleep 15
softflowd -i eth0 -v 9 -n monitor.dev:2055

# Start MiNiFi-cpp
sed -i "s/nifi\.server\.report\.interval=1000 ms/nifi\.server\.report\.interval=0 ms/g" $MINIFI_HOME/conf/minifi.properties
cd $MINIFI_HOME
minifi &

# Start web app script
source /scripts/$SCRIPT
