INTERVAL=$1
HOSTNAME=$(hostname -f)

DIR=/host-data/metrics/ps/$HOSTNAME
mkdir -p $DIR

while true
do 
  DATE=$(date +%s)
  ps aux >> $DIR/$DATE
  sleep $INTERVAL
done
