import logging

from data_stack.governance.quality import DataQualityRule
from data_stack.models.data_asset.table.table import Database, Catalog, TableEngine, TableSchema, TableField, DwdTable
from data_stack.models.job.base_job import Job
from data_warehouse.layers.ods.ods_stock_market_s_d import ods_stock_market_s_d

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


class DwdStockMarketSDJob(Job):
    """
    DWD Stock Market Snapshot Daily job
    """
    name = "dwd_stock_market_s_d"

    inputs = [
        ods_stock_market_s_d
    ]
    output = dwd_stock_market_s_d

    def process(self):
        logging.info(f"Reading from {self.inputs}")
        ods_df = self.spark.read.table(self.inputs[0].full_name())
        logging.info(f"Transforming")

        dwd_df = ods_df

        from data_stack.utils import dataframe_writer
        dataframe_writer.write_to_table(dwd_df, self.output, partition_columns=["partition_date"])

        logging.info(f"Saved to {self.output}")

