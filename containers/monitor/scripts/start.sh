#!/bin/bash
#set -eu

MASTER_FQDN=monitor.dev
echo "export NIFI_HOME=/nifi" >> /root/.bashrc
echo "export HOSTNAME=$(hostname -f)" >> /root/.bashrc
echo "export IP=$(hostname -i)" >> /root/.bashrc
echo "export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk" >> /root/.bashrc
source /root/.bashrc

# Setup and start NiFi
PROTO_PORT=1025
SOCKET_PORT=1026
sed -i "s/protocol\.port=/protocol\.port=$PROTO_PORT/g" $NIFI_HOME/conf/nifi.properties
sed -i "s/node\.address=/node\.address=$HOSTNAME/g" $NIFI_HOME/conf/nifi.properties
sed -i "s/manager\.address=/manager\.address=$MASTER_FQDN/g" $NIFI_HOME/conf/nifi.properties
sed -i "s/http.host=/http\.host=$HOSTNAME/g" $NIFI_HOME/conf/nifi.properties
# Sets up site-to-site for INSECURE communication
sed -i "s/input.secure=true/input\.secure=false/g" $NIFI_HOME/conf/nifi.properties
sed -i "s/input.socket.port=/input\.socket\.port=$SOCKET_PORT/g" $NIFI_HOME/conf/nifi.properties
sed -i "s/input.socket.host=/input\.socket\.host=$HOSTNAME/g" $NIFI_HOME/conf/nifi.properties

#sed -i "s/is\.manager=false/is\.manager=true/g" $NIFI_HOME/conf/nifi.properties
#sed -i "s/is\.node=true/is\.node=false/g" $NIFI_HOME/conf/nifi.properties
$NIFI_HOME/bin/nifi.sh start
sleep 5
tail -f $NIFI_HOME/logs/nifi-app.log
