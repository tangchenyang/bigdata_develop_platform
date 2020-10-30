#!/bin/bash
sqoop list-databases \
--connect jdbc:mysql://hadoop:3306/tcy_db?characterEncoding=UTF-8 \
--username root \
--password '123456'
