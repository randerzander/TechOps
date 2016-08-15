FROM centos
ARG NIFI_URL
ARG HDF_HOME
RUN yum install -y java-1.8.0-openjdk-devel net-tools wget

RUN mkdir /etc/consul.d
ADD bin/consul /usr/bin/consul

RUN wget -nv ${NIFI_URL} -O /nifi.tgz
RUN tar -xzvf /nifi.tgz
RUN mv ${HDF_HOME}/nifi /

ADD bin/minifi /usr/bin/minifi
ADD minifi /minifi

ADD bin/nmon /usr/bin/nmon
RUN mkdir /nmon

RUN mkdir /logs

ADD scripts /scripts
CMD sh /scripts/start.sh $MASTER $HOSTNAME
