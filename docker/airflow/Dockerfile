FROM ubuntu:latest

USER root

# set timezone
RUN ln -snf /usr/share/zoneinfo/Hongkong /etc/localtime
ARG DEBIAN_FRONTEND=noninteractive

# update apt
RUN sed -i "s@ports.ubuntu.com@mirrors.aliyun.com@g" /etc/apt/sources.list
RUN apt clean && apt update

# install
RUN apt install -y vim tree

# install postgres
RUN apt install -y postgresql postgresql-contrib

# install python
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3.9 python3-pip

# install airflow
RUN pip install apache-airflow==2.4.3 psycopg2-binary -c https://raw.githubusercontent.com/apache/airflow/constraints-2.4.3/constraints-3.9.txt
ENV AIRFLOW_HOME=/root/airflow
ENV OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

# setup for fox poject
RUN mkdir -p /root/software
## set up postgres
ADD setup_postgres.sh /root/software/
RUN bash /root/software/setup_postgres.sh

## setup airflow
ADD setup_airflow.sh /root/software/
RUN bash /root/software/setup_airflow.sh

ADD bootstrap.sh /root/software/

# Airflow port
EXPOSE 8080
# Postgres port
EXPOSE 5432

CMD ["bash", "/root/software/bootstrap.sh", "-d"]
