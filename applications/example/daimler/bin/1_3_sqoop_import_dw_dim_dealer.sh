#!/bin/bash
query="SELECT * FROM dw_dim_dealer WHERE \$CONDITIONS"
bash util/sqoop-import-daimler.sh "$query" "default" "dw_dim_dealer"