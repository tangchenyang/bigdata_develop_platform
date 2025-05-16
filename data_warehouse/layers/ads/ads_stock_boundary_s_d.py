from datetime import date

from pyspark.sql.functions import max as f_max, min as f_min, lit

from data_stack.models.data_asset.table.table import TableSchema, TableField, AdsTable, Database, Catalog, TableEngine
from data_stack.models.job.base_job import Job
from data_warehouse.layers.dws.dws_stock_market_s_d import dws_stock_market_s_d

ads_stock_boundary_s_d_schema = TableSchema(
    fields=[
        TableField("stock_code", "STRING", "股票代码", ["NOT_NULL", "UNIQUE"]),
        TableField("stock_name", "STRING", "股票名称", ["NOT_NULL"]),
        TableField("lowest", "STRING", "最低价", ["NOT_NULL"]),
        TableField("highest", "STRING", "最高价", ["NOT_NULL"]),
        TableField("partition_date", "STRING", "分区日期"),
    ],
    partition_fields=["partition_date"],
)

ads_stock_boundary_s_d = AdsTable(
    name="ads_stock_boundary_s_d",
    database=Database.ADS,
    catalog=Catalog.ICEBERG_CATALOG,
    engine=TableEngine.ICEBERG,
    schema=ads_stock_boundary_s_d_schema,
)


class AdsStockBoundarySDJob(Job):
    name = "ads_stock_boundary_s_d"

    inputs = [dws_stock_market_s_d]

    output = ads_stock_boundary_s_d

    def process(self):
        from data_stack.utils import dataframe_reader, dataframe_writer

        dws_stock_market_df = dataframe_reader.read_from_table(self.inputs[0], self.spark)

        current_date = date.today().strftime("%Y-%m-%d")  # todo consider pass from execution params
        ads_stock_boundary = (
            dws_stock_market_df
            .groupBy("stock_code", "stock_name")
            .agg(f_min("low").alias("lowest"), f_max("high").alias("highest"))
            .withColumn("partition_date", lit(current_date))
        )

        dataframe_writer.write_to_table(ads_stock_boundary, self.output)
