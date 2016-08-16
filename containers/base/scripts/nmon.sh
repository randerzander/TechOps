INTERVAL=$1
HOSTNAME=$(hostname -f)

DIR=/host-data/metrics/nmon/$HOSTNAME
mkdir -p $DIR

while true
do 
  DATE=$(date +%s)
  nmon -f -s1 -c1 -m $DIR
  sleep $INTERVAL
done
