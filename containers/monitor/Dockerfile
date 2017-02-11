FROM centos

RUN yum install -y java-1.8.0-openjdk-devel
RUN yum install -y net-tools
RUN yum install -y bind-utils
RUN yum install -y wget
RUN yum install -y unzip

# NiFi Controller
ARG NIFI_URL
ARG NIFI_SUBFOLDER
#RUN wget -nv ${NIFI_URL} -O /nifi.tgz
COPY ${NIFI_URL} /nifi.tgz
RUN tar -xzvf /nifi.tgz
# HDF is shipped as ${NIFI_SUBFOLDER/nifi}, Apache NiFi is shipped with no subfolder
#RUN mv ${NIFI_SUBFOLDER}/nifi /nifi
RUN mv ${NIFI_SUBFOLDER} /nifi

ADD scripts /scripts
ADD flow.xml.gz /nifi/conf/flow.xml.gz
CMD sh /scripts/start.sh
