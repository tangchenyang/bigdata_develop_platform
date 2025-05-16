import logging

from data_stack.models.data_asset.table.table import Database, Catalog, TableEngine, TableSchema, TableField, DwdTable
from data_stack.models.job.base_job import Job
from data_warehouse.layers.ods.ods_stock_market_s_d import ods_stock_market_s_d

dwd_stock_market_s_d_schema_v1 = TableSchema(
    fields=[
        TableField("date", "DATE", "日期", ["NOT_NULL"]),
        TableField("open", "DOUBLE", "开盘价", ["NOT_NULL"]),
        TableField("high", "DOUBLE", "最高价", ["NOT_NULL"]),
        TableField("low", "DOUBLE", "最低价", ["NOT_NULL"]),
        TableField("close", "DOUBLE", "收盘价", ["NOT_NULL"]),
        TableField("volume", "DOUBLE", "成交量", ["NOT_NULL"]),
        TableField("amount", "DOUBLE", "成交额", ["NOT_NULL"]),
        TableField("outstanding_share", "DOUBLE", "流通股", ["NOT_NULL"]),
        TableField("turnover", "DOUBLE", "换手率", ["NOT_NULL"]),
        TableField("stock_code", "DOUBLE", "股票代码", ["NOT_NULL"]),
        TableField("partition_date", "STRING", "分区日期"),
    ],
    partition_fields=[
        "partition_date"
    ]
)

dwd_stock_market_s_d_schema_v2 = dwd_stock_market_s_d_schema_v1.add(
    TableField("ingest_time", "DOUBLE", "采集时间", ["NOT_NULL"]),
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
        from data_stack.utils import dataframe_reader
        ods_df = dataframe_reader.read_from_table(self.inputs[0], self.spark)

        dwd_df = ods_df

        from data_stack.utils import dataframe_writer
        dataframe_writer.write_to_table(dwd_df, self.output)


