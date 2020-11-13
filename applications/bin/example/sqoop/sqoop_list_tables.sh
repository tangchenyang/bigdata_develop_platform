#!/bin/bash
sqoop list-tables \
--connect jdbc:mysql://hadoop:3306/test_db?characterEncoding=UTF-8 \
--username root \
--password '123456'
