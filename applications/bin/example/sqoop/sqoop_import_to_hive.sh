#!/bin/bash
mysql -uroot -p123456 <<EOF
create database test_db;
create table test_db.test_table_person ( name varchar(32), age int);
insert into test_db.test_table_person values ('Person-1',18);
insert into test_db.test_table_person values ('Person-2',18);
insert into test_db.test_table_person values ('Person-3',18);
insert into test_db.test_table_person values ('Person-4',20);
insert into test_db.test_table_person values ('Person-5',20);
insert into test_db.test_table_person values ('Person-6',20);
EOF

hive -e "create database if not exists ods"

uuidgen=`uuidgen`
tmp_dir="${SQOOP_HOME}/tmp/uuidgen"
sqoop import \
--connect jdbc:mysql://hadoop:3306/test_db \
--username root \
--password '123456' \
--query 'select name, age from test_db.test_table_person where $CONDITIONS' \
--hive-import \
--hive-overwrite \
--hive-database ods \
--hive-table test_person \
--target-dir /user/hive/wa/ \
--delete-target-dir \
--bindir ${tmp_dir} \
--outdir ${tmp_dir} \
-m 1
