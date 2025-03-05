import logging
from functools import reduce

from pyspark.sql import DataFrame
from pyspark.sql.functions import expr

from data_stack.models.job.base_job import Job
from data_warehouse.tables import tables


class OdsStockMarketSD(Job):
    name = "ods_stock_market_s_d"

    inputs = []
    output = tables.ods_stock_market_s_d

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

