#!/bin/bash
query="SELECT * FROM deal_item_list WHERE \$CONDITIONS"
bash util/sqoop-import-daimler.sh "$query" "default" "ods_deal_item_list"