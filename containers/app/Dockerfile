FROM centos

RUN yum install -y java-1.8.0-openjdk-devel
RUN yum install -y net-tools
RUN yum install -y bind-utils
RUN yum install -y wget
RUN yum install -y unzip
RUN yum install -y epel-release
RUN yum install -y leveldb-devel
RUN yum install -y libpcap-devel

# NMon
ARG NMON_URL=http://sourceforge.net/projects/nmon/files/nmon16e_x86_rhel72

RUN wget -nv ${NMON_URL} -O /usr/bin/nmon
RUN chmod +x /usr/bin/nmon

# MiNiFi-cpp
ADD bin/minifi /usr/bin/minifi
ADD minifi /minifi

ADD bin/softflowd /usr/bin/softflowd
ADD bin/softflowctl /usr/bin/softflowctl

# Setup Data Directories
RUN mkdir -p /host-data/logs
RUN mkdir -p /host-data/metrics/nmon
RUN mkdir -p /host-data/metrics/ps
RUN mkdir -p /host-data/metrics/netstat

ADD scripts /scripts
CMD sh /scripts/start.sh
