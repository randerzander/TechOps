FROM centos
ARG SPARK_URL
ARG SPARK_SUBFOLDER
ARG ZEPPELIN_URL
ARG ZEPPELIN_SUBFOLDER
RUN yum install -y java-1.8.0-openjdk-devel net-tools wget unzip git

# Spark bits
RUN wget -nv ${SPARK_URL} -O /spark.tgz
RUN tar -xzvf /spark.tgz
RUN mv ${SPARK_SUBFOLDER} /spark

# Zeppelin bits
RUN wget -nv ${ZEPPELIN_URL} -O /zeppelin.tgz
RUN tar -xzvf /zeppelin.tgz
RUN mv ${ZEPPELIN_SUBFOLDER} /zeppelin
ADD notebook /zeppelin/notebook

# Spark conf
RUN cp /spark/conf/spark-defaults.conf.template /spark/conf/spark-defaults.conf
RUN echo "spark.sql.warehouse.dir /data/derived" >> /spark/conf/spark-defaults.conf

# Zeppelin conf
RUN cp /zeppelin/conf/zeppelin-env.sh.template /zeppelin/conf/zeppelin-env.sh
RUN echo "export SPARK_HOME=/spark" >> /zeppelin/conf/zeppelin-env.sh

CMD sh /zeppelin/bin/zeppelin-daemon.sh start; tail -f /zeppelin/logs/zeppelin-*.log
