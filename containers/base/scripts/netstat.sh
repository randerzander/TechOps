INTERVAL=$1
HOSTNAME=$(hostname -f)

DIR=/host-data/metrics/netstat/$HOSTNAME
mkdir -p $DIR

while true
do 
  DATE=$(date +%s)
  netstat -Wape >> $DIR/$DATE
  sleep $INTERVAL
done
