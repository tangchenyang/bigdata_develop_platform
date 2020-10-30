#!/bin/bash
spark-sql -f example_build_table.sql --hivevar app_home=${APPLICATIONS_HOME}


