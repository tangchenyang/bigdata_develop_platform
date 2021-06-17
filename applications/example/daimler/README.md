example: 根据某销售数据建设数仓，报表统计
# batch
### 0 准备测试数据，写入 mysql
```shell script
bash 0_init_mysql.sh
```
### 1 通过sqoop 将 Mysql 的数据导入到 Hive 的 ODS层 
```shell script
bash  1_1_sqoop_import_ods_deal_record.sh
bash  1_2_sqoop_import_ods_deal_item_list.sh
bash  1_3_sqoop_import_dw_dim_dealer.sh  
```

### 2 通过 spark 程序做etl 形成 fact 表
```shell script
bash 2_1_spark_dw_fact_sales_deal_record.sh
bash 2_2_spark_dw_fact_sales_deal_item_list.sh
```

### 3 通过 spark 程序做报表统计，形成 dm 表
```shell script
bash 3_1_spark_dw_dm_sales_top1_item_on_dealer.sh
```

### 4 通过 sqoop 将 dm 表的数据导出到 MySQL， 作为数据集市供应用查询
```shell script
sqoop export dw_dm_xxx
```


 