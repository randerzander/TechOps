FROM centos
ARG NIFI_URL
ARG NIFI_SUBFOLDER
RUN yum install -y java-1.8.0-openjdk-devel net-tools wget unzip

RUN wget -nv ${NIFI_URL} -O /nifi.tgz
RUN tar -xzvf /nifi.tgz
RUN mv ${NIFI_SUBFOLDER}/nifi /nifi

RUN mkdir /etc/consul.d
ADD bin/consul /usr/bin/consul
ADD bin/nmon /usr/bin/nmon

ADD bin/minifi /usr/bin/minifi
ADD minifi /minifi
ADD flow.xml.gz /nifi/conf/

RUN mkdir -p /host-data/logs
RUN mkdir -p /host-data/metrics/nmon
RUN mkdir -p /host-data/metrics/ps
RUN mkdir -p /host-data/metrics/netstat

ADD scripts /scripts
CMD sh /scripts/start.sh $MASTER $HOSTNAME
