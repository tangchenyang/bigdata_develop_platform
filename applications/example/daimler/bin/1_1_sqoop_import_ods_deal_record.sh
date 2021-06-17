#!/bin/bash
query="SELECT * FROM deal_record WHERE \$CONDITIONS"
bash util/sqoop-import-daimler.sh "$query" "default" "ods_deal_record"