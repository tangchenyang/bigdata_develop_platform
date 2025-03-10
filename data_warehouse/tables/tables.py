from data_stack.governance.quality import DataQualityRule
from data_stack.models.data_asset.table.table import OdsTable, DwdTable, Database, Catalog, TableEngine, TableSchema, TableField

ods_stock_market_s_d = OdsTable(
    "ods_stock_market_s_d",
    database=Database.ODS,
    catalog=Catalog.ICEBERG_CATALOG,
    engine=TableEngine.ICEBERG,
    schema=TableSchema(
        fields=[
            TableField("date", "DATE", "日期", [DataQualityRule.NOT_NULL]),
            TableField("open", "DOUBLE", "开盘价", [DataQualityRule.NOT_NULL]),
            TableField("high", "DOUBLE", "最高价", [DataQualityRule.NOT_NULL]),
            TableField("low", "DOUBLE", "最低价", [DataQualityRule.NOT_NULL]),
            TableField("close", "DOUBLE", "收盘价", [DataQualityRule.NOT_NULL]),
            TableField("volume", "DOUBLE", "成交量", [DataQualityRule.NOT_NULL]),
            TableField("amount", "DOUBLE", "成交额", [DataQualityRule.NOT_NULL]),
            TableField("outstanding_share", "DOUBLE", "流通股", [DataQualityRule.NOT_NULL]),
            TableField("turnover", "DOUBLE", "换手率", [DataQualityRule.NOT_NULL]),
            TableField("stock_code", "DOUBLE", "股票代码", [DataQualityRule.NOT_NULL]),
            TableField("ingest_time", "DOUBLE", "采集时间", [DataQualityRule.NOT_NULL]),
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
            TableField("stock_exchange", "STRING", "证券交易所", [DataQualityRule.NOT_NULL]),
            TableField("stock_code", "STRING", "股票代码", [DataQualityRule.NOT_NULL, DataQualityRule.UNIQUE]),
            TableField("stock_name", "STRING", "股票名称", [DataQualityRule.NOT_NULL]),
            TableField("company_name", "STRING", "公司名称", [DataQualityRule.NOT_NULL]),
            TableField("industry", "STRING", "所属行业", [DataQualityRule.NOT_NULL]),
            TableField("listing_date", "STRING", "上市日期", [DataQualityRule.NOT_NULL]),
            TableField("ingest_time", "TIMESTAMP", "采集时间", [DataQualityRule.NOT_NULL]),
        ],
        partition_fields=[
            "partition_date"
        ]

    )
)
dwd_stock_market_s_d_schema_v1 = TableSchema(
        fields=[
            TableField("date", "DATE", "日期", [DataQualityRule.NOT_NULL]),
            TableField("open", "DOUBLE", "开盘价", [DataQualityRule.NOT_NULL]),
            TableField("high", "DOUBLE", "最高价", [DataQualityRule.NOT_NULL]),
            TableField("low", "DOUBLE", "最低价", [DataQualityRule.NOT_NULL]),
            TableField("close", "DOUBLE", "收盘价", [DataQualityRule.NOT_NULL]),
            TableField("volume", "DOUBLE", "成交量", [DataQualityRule.NOT_NULL]),
            TableField("amount", "DOUBLE", "成交额", [DataQualityRule.NOT_NULL]),
            TableField("outstanding_share", "DOUBLE", "流通股", [DataQualityRule.NOT_NULL]),
            TableField("turnover", "DOUBLE", "换手率", [DataQualityRule.NOT_NULL]),
            TableField("stock_code", "DOUBLE", "股票代码", [DataQualityRule.NOT_NULL]),
        ],
        partition_fields=[
            "partition_date"
        ]
    )
dwd_stock_market_s_d_schema_v2 = dwd_stock_market_s_d_schema_v1.add(
    TableField("ingest_time", "DOUBLE", "采集时间", [DataQualityRule.NOT_NULL]),
)

dwd_stock_market_s_d = DwdTable(
    "dwd_stock_market_s_d",
    database=Database.DWD,
    catalog=Catalog.ICEBERG_CATALOG,
    engine=TableEngine.ICEBERG,
    schema=dwd_stock_market_s_d_schema_v2
)
# todo consider schema evolution
