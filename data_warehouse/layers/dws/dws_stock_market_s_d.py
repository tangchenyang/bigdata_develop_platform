from pyspark.sql.functions import right, lit

from data_stack.models.data_asset.table.table import TableSchema, TableField, DwsTable, Database, Catalog, TableEngine
from data_stack.models.job.base_job import Job
from data_warehouse.layers.dim.dim_stock import dim_stock
from data_warehouse.layers.dwd.dwd_stock_market_s_d import dwd_stock_market_s_d

dws_stock_market_s_d_schema = TableSchema(
    fields=[
        TableField("date", "DATE", "日期", ["NOT_NULL"]),
        TableField("stock_code", "STRING", "股票代码", ["NOT_NULL"]),
        TableField("stock_name", "STRING", "股票名称", ["NOT_NULL"]),
        TableField("stock_exchange", "STRING", "证券交易所", ["NOT_NULL"]),
        TableField("company_name", "STRING", "公司名称", ["NOT_NULL"]),
        TableField("industry", "STRING", "所属行业", ["NOT_NULL"]),
        TableField("listing_date", "STRING", "上市日期", ["NOT_NULL"]),
        TableField("open", "DOUBLE", "开盘价", ["NOT_NULL"]),
        TableField("high", "DOUBLE", "最高价", ["NOT_NULL"]),
        TableField("low", "DOUBLE", "最低价", ["NOT_NULL"]),
        TableField("close", "DOUBLE", "收盘价", ["NOT_NULL"]),
        TableField("volume", "DOUBLE", "成交量", ["NOT_NULL"]),
        TableField("amount", "DOUBLE", "成交额", ["NOT_NULL"]),
        TableField("outstanding_share", "DOUBLE", "流通股", ["NOT_NULL"]),
        TableField("turnover", "DOUBLE", "换手率", ["NOT_NULL"]),
        TableField("partition_date", "STRING", "分区日期"),
    ],
    partition_fields=[
        "partition_date"
    ]
)
dws_stock_market_s_d = DwsTable(
    name="dws_stock_market_s_d",
    database=Database.DWS,
    catalog=Catalog.ICEBERG_CATALOG,
    engine=TableEngine.ICEBERG,
    schema=dws_stock_market_s_d_schema,
)


class DwsStockMarketSDJob(Job):
    name = "dws_stock_market_s_d"
    inputs = [
        dim_stock,
        dwd_stock_market_s_d,
    ]
    output = dws_stock_market_s_d

    def process(self):
        from data_stack.utils import dataframe_writer, dataframe_reader
        dim_stock_df = dataframe_reader.read_from_table(self.inputs[0], self.spark)
        dwd_stock_market_df = dataframe_reader.read_from_table(self.inputs[1], self.spark)
        dwd_stock_market_df = dwd_stock_market_df.withColumn("stock_code", right("stock_code", lit(6)))

        dws_stock_market_df = dwd_stock_market_df.join(dim_stock_df, on="stock_code", how="inner")

        dataframe_writer.write_to_table(dws_stock_market_df, self.output)
