#!/bin/bash
#set -eu

MASTER_FQDN=monitor.dev
NIFI_HOME=/nifi
MINIFI_HOME=/minifi
HOSTNAME=$(hostname -f)
IP=$(hostname -i)
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk

# Setup and start NiFi
echo "export NIFI_HOME=$NIFI_HOME" >> /root/.bashrc
PROTO_PORT=1025
SOCKET_PORT=1026
sed -i "s/protocol\.port=/protocol\.port=$PROTO_PORT/g" $NIFI_HOME/conf/nifi.properties
sed -i "s/protocol\.port=/protocol\.port=$PROTO_PORT/g" $MINIFI_HOME/conf/minifi.properties
sed -i "s/node\.address=/node\.address=$HOSTNAME/g" $NIFI_HOME/conf/nifi.properties
sed -i "s/node\.address=/node\.address=$HOSTNAME/g" $MINIFI_HOME/conf/minifi.properties
sed -i "s/manager\.address=/manager\.address=$MASTER_FQDN/g" $NIFI_HOME/conf/nifi.properties
sed -i "s/manager\.address=/manager\.address=$MASTER_FQDN/g" $MINIFI_HOME/conf/minifi.properties
sed -i "s/http.host=/http\.host=$HOSTNAME/g" $NIFI_HOME/conf/nifi.properties
sed -i "s/http.host=/http\.host=$HOSTNAME/g" $MINIFI_HOME/conf/minifi.properties
# Sets up site-to-site for INSECURE communication
sed -i "s/input.secure=true/input\.secure=false/g" $NIFI_HOME/conf/nifi.properties
sed -i "s/input.secure=true/input\.secure=false/g" $MINIFI_HOME/conf/minifi.properties
sed -i "s/input.socket.port=/input\.socket\.port=$SOCKET_PORT/g" $NIFI_HOME/conf/nifi.properties
sed -i "s/input.socket.port=/input\.socket\.port=$SOCKET_PORT/g" $MINIFI_HOME/conf/minifi.properties
sed -i "s/input.socket.host=/input\.socket\.host=$HOSTNAME/g" $NIFI_HOME/conf/nifi.properties
sed -i "s/input.socket.host=/input\.socket\.host=$HOSTNAME/g" $MINIFI_HOME/conf/minifi.properties
if [ $MODE = "master" ]; then
  sed -i "s/is\.manager=false/is\.manager=true/g" $NIFI_HOME/conf/nifi.properties
  sed -i "s/is\.manager=false/is\.manager=true/g" $MINIFI_HOME/conf/minifi.properties
  sed -i "s/is\.node=true/is\.node=false/g" $NIFI_HOME/conf/nifi.properties
  sed -i "s/is\.node=true/is\.node=false/g" $MINIFI_HOME/conf/minifi.properties
  $NIFI_HOME/bin/nifi.sh start
else
  sed -i "s/is\.manager=true/is\.manager=false/g" $NIFI_HOME/conf/nifi.properties
  sed -i "s/is\.manager=true/is\.manager=false/g" $MINIFI_HOME/conf/minifi.properties
  sed -i "s/is\.node=false/is\.node=true/g" $NIFI_HOME/conf/nifi.properties
  sed -i "s/is\.node=false/is\.node=true/g" $MINIFI_HOME/conf/minifi.properties
  sed -i "s/nifi\.server\.name=localhost/nifi\.server\.name=$MASTER_FQDN/g" $MINIFI_HOME/conf/minifi.properties
  sed -i "s/nifi\.server\.port=9000/nifi\.server\.port=$PROTO_PORT/g" $MINIFI_HOME/conf/minifi.properties
  #cd $MINIFI_HOME
  #minifi &
  $NIFI_HOME/bin/nifi.sh start
fi

# Setup and start Consul
if [ $MODE = "master" ]; then
  echo "I am MODE: $MODE, $MASTER_FQDN"
  consul agent -server -dev -bootstrap-expect 1 -bind 0.0.0.0 -client 0.0.0.0 -ui
else
  echo "I am MODE: $MODE, $MASTER_FQDN"
  source /scripts/$SCRIPT
  sleep 10
  consul agent -config-dir /etc/consul.d -dev -join $MASTER_FQDN
fi
