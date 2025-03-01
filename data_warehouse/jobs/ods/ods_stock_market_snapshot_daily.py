import logging

from pyspark.sql.functions import expr

from data_stack.models.job.base_job import Job
from data_warehouse.tables import tables


class OdsStockMarketSnapshotDaily(Job):
    name = "ods_stock_market_snapshot_daily"

    inputs = []
    output = tables.ods_stock_market_snapshot_daily

    def process(self):
        stock_codes = ["sh600519", "sz002594"]

        for stock_code in stock_codes:
            from data_warehouse.services import stock_service
            pd_df = stock_service.get_stock_daily(stock_code)

            spark_df = self.spark.createDataFrame(pd_df)
            spark_df = spark_df.withColumn("partition_date", expr("TO_DATE(timestamp)"))

            from data_stack.utils import dataframe_writer
            dataframe_writer.write_to_table(spark_df, self.output, partition_columns=["partition_date"])

        logging.info(f"Saved to {self.output}")

