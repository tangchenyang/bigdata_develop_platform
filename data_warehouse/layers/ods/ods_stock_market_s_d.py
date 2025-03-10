import logging
from functools import reduce

from pyspark.sql import DataFrame
from pyspark.sql.functions import expr

from data_stack.governance.quality import DataQualityRule
from data_stack.models.data_asset.table.table import OdsTable, Database, Catalog, TableEngine, TableSchema, TableField
from data_stack.models.job.base_job import Job

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


class OdsStockMarketSDJob(Job):
    name = "ods_stock_market_s_d"

    inputs = []
    output = ods_stock_market_s_d

    def process(self):
        stock_codes = ["sh600519", "sz002594"]
        stock_dfs: list[DataFrame] = []
        for stock_code in stock_codes:
            from data_warehouse.services import stock_service
            pd_df = stock_service.get_stock_daily(stock_code)

            spark_df = self.spark.createDataFrame(pd_df)
            spark_df = spark_df.withColumn("partition_date", expr("TO_DATE(ingest_time)"))
            stock_dfs.append(spark_df)

        stock_df = reduce(lambda df1, df2: df1.union(df2), stock_dfs)

        from data_stack.utils import dataframe_writer
        dataframe_writer.write_to_table(stock_df, self.output, partition_columns=["partition_date"])
        logging.info(f"Saved to {self.output}")

