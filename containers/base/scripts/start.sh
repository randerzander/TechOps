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
echo "export MINIFI_HOME=$MINIFI_HOME" >> /root/.bashrc
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
if [ $MODE = "master" ]; then
  #sed -i "s/is\.manager=false/is\.manager=true/g" $NIFI_HOME/conf/nifi.properties
  #sed -i "s/is\.node=true/is\.node=false/g" $NIFI_HOME/conf/nifi.properties
  $NIFI_HOME/bin/nifi.sh start
#else
  #sed -i "s/is\.manager=true/is\.manager=false/g" $NIFI_HOME/conf/nifi.properties
  #$NIFI_HOME/bin/nifi.sh start
fi

# Start web app script
source /scripts/$SCRIPT

echo "I am MODE: $HOSTNAME, $MODE"
if [ $MODE = "master" ]; then
  consul agent -server -dev -bootstrap-expect 1 -bind 0.0.0.0 -client 0.0.0.0 -ui
else
  # Let mmonitor start consul and NiFi collector
  sleep 35
  # Start MiNiFi-cpp
  sed -i "s/is\.node=false/is\.node=true/g" $NIFI_HOME/conf/nifi.properties
  sed -i "s/nifi\.server\.report\.interval=1000 ms/nifi\.server\.report\.interval=0 ms/g" $MINIFI_HOME/conf/minifi.properties
  cd $MINIFI_HOME
  minifi &

  # Start metrics scripts
  sh /scripts/ps.sh 5 &
  sh /scripts/netstat.sh 5 &
  sh /scripts/nmon.sh 15 &

  consul agent -config-dir /etc/consul.d -dev -retry-join $MASTER_FQDN
fi
