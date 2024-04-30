#!/bin/bash
service postgresql start

# create role/db for airflow
su - postgres <<EOF
psql -c "ALTER USER postgres PASSWORD 'postgres';"

psql -c "CREATE USER airflow WITH PASSWORD 'airflow';"
psql -c "CREATE DATABASE airflow OWNER airflow;"
psql -c "ALTER DATABASE airflow OWNER TO airflow;"
psql -c "GRANT ALL PRIVILEGES ON DATABASE airflow to airflow;"
psql -c "CREATE DATABASE airflow_ctl OWNER airflow;"
psql -c "ALTER DATABASE airflow_ctl OWNER TO airflow;"
psql -c "GRANT ALL PRIVILEGES ON DATABASE airflow_ctl to airflow;"
EOF

# set access config
sed -i "s/peer/md5/g" /etc/postgresql/14/main/pg_hba.conf
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/g" /etc/postgresql/14/main/postgresql.conf
echo "# allow all access from any host" /etc/postgresql/14/main/pg_hba.conf
echo "host    all             all             0.0.0.0/0               md5" /etc/postgresql/14/main/pg_hba.conf
service postgresql restart

# create table for airflow
su - postgres << EOF
PGPASSWORD=airflow psql airflow_ctl -U airflow -w -c "
CREATE TABLE control_tbl
(
    control_id     BIGSERIAL PRIMARY KEY NOT NULL,
    airflow_dag_id varchar(250)          NOT NULL,
    airflow_run_id varchar(250)          NOT NULL,
    start_time     BIGINT,
    end_time       BIGINT,
    status         varchar(25),
    has_errors     boolean,
    errors         TEXT,
    extra_info     TEXT,
    created_at     TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'UTC'),
    last_updated   TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'UTC')
);
"
EOF
