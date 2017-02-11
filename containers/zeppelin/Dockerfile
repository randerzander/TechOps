FROM app

RUN yum install -y git

# Spark bits
ARG SPARK_URL
ARG SPARK_SUBFOLDER
RUN wget -nv ${SPARK_URL} -O /spark.tgz
#COPY ${SPARK_URL} /spark.tgz
RUN tar -xzvf /spark.tgz
RUN mv ${SPARK_SUBFOLDER} /spark

# Zeppelin bits
ARG ZEPPELIN_URL
ARG ZEPPELIN_SUBFOLDER
RUN wget -nv ${ZEPPELIN_URL} -O /zeppelin.tgz
#COPY ${ZEPPELIN_URL} /zeppelin.tgz
RUN tar -xzvf /zeppelin.tgz
RUN mv ${ZEPPELIN_SUBFOLDER} /zeppelin

# Spark conf
RUN cp /spark/conf/spark-defaults.conf.template /spark/conf/spark-defaults.conf
RUN echo "spark.sql.warehouse.dir /data/derived" >> /spark/conf/spark-defaults.conf

# Zeppelin conf
RUN cp /zeppelin/conf/zeppelin-env.sh.template /zeppelin/conf/zeppelin-env.sh
RUN echo "export SPARK_HOME=/spark" >> /zeppelin/conf/zeppelin-env.sh

CMD sh /zeppelin/bin/zeppelin-daemon.sh start; sleep 5; tail -f /zeppelin/logs/zeppelin-*.log
