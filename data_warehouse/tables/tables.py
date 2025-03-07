from data_stack.models.data_asset.table.table import OdsTable, DwdTable, Database, Catalog, TableEngine, TableSchema, TableField

ods_stock_market_s_d = OdsTable(
    "ods_stock_market_s_d",
    database=Database.ODS,
    catalog=Catalog.ICEBERG_CATALOG,
    engine=TableEngine.ICEBERG,
    schema=TableSchema(
        fields=[
            TableField("date", "DATE", "日期", ["Not Null"]),
            TableField("open", "DOUBLE", "开盘价", ["Not Null"]),
            TableField("high", "DOUBLE", "最高价", ["Not Null"]),
            TableField("low", "DOUBLE", "最低价", ["Not Null"]),
            TableField("close", "DOUBLE", "收盘价", ["Not Null"]),
            TableField("volume", "DOUBLE", "成交量", ["Not Null"]),
            TableField("amount", "DOUBLE", "成交额", ["Not Null"]),
            TableField("outstanding_share", "DOUBLE", "流通股", ["Not Null"]),
            TableField("turnover", "DOUBLE", "换手率", ["Not Null"]),
            TableField("stock_code", "DOUBLE", "股票代码", ["Not Null"]),
            TableField("ingest_time", "DOUBLE", "采集时间", ["Not Null"]),
        ],
        partition_fields=[
            "partition_date"
        ]
    )
)

ods_stock_info_s_d = OdsTable(
    "ods_stock_info_s_d",
    database=Database.ODS,
    catalog=Catalog.ICEBERG_CATALOG,
    engine=TableEngine.ICEBERG,
    schema=TableSchema(
        fields=[
            TableField("stock_exchange", "STRING", "证券交易所", ["Not Null"]),
            TableField("stock_code", "STRING", "股票代码", ["Not Null", "Unique"]),
            TableField("stock_name", "STRING", "股票名称", ["Not Null"]),
            TableField("company_name", "STRING", "公司名称", ["Not Null"]),
            TableField("industry", "STRING", "所属行业", ["Not Null"]),
            TableField("listing_date", "STRING", "上市日期", ["Not Null"]),
            TableField("ingest_time", "TIMESTAMP", "采集时间", ["Not Null"]),
        ],
        partition_fields=[
            "partition_date"
        ]

    )
)
dwd_stock_market_s_d_schema_v1 = TableSchema(
        fields=[
            TableField("date", "DATE", "日期", ["Not Null"]),
            TableField("open", "DOUBLE", "开盘价", ["Not Null"]),
            TableField("high", "DOUBLE", "最高价", ["Not Null"]),
            TableField("low", "DOUBLE", "最低价", ["Not Null"]),
            TableField("close", "DOUBLE", "收盘价", ["Not Null"]),
            TableField("volume", "DOUBLE", "成交量", ["Not Null"]),
            TableField("amount", "DOUBLE", "成交额", ["Not Null"]),
            TableField("outstanding_share", "DOUBLE", "流通股", ["Not Null"]),
            TableField("turnover", "DOUBLE", "换手率", ["Not Null"]),
            TableField("stock_code", "DOUBLE", "股票代码", ["Not Null"]),
        ],
        partition_fields=[
            "partition_date"
        ]
    )
dwd_stock_market_s_d_schema_v2 = dwd_stock_market_s_d_schema_v1.add(
    TableField("ingest_time", "DOUBLE", "采集时间", ["Not Null"]),
)

dwd_stock_market_s_d = DwdTable(
    "dwd_stock_market_s_d",
    database=Database.DWD,
    catalog=Catalog.ICEBERG_CATALOG,
    engine=TableEngine.ICEBERG,
    schema=dwd_stock_market_s_d_schema_v2
)
# todo consider schema evolution
