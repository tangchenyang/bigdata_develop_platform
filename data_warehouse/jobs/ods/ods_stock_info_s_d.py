import logging

from pyspark.sql.functions import expr

from data_stack.models.job.base_job import Job
from data_warehouse.tables import tables


class OdsStockInfoSD(Job):
    """
    ODS Stock Info Snapshot Daily job
    """
    name = "ods_stock_info_s_d"

    inputs = []
    output = tables.ods_stock_info_s_d

    def process(self):
        from data_warehouse.services import stock_service

        stock_info_pd_df = stock_service.get_all_stock_list()
        stock_info_df = self.spark.createDataFrame(stock_info_pd_df)

        from data_stack.utils import dataframe_writer
        stock_info_df = stock_info_df.withColumn("partition_date", expr("TO_DATE(timestamp)"))
        dataframe_writer.write_to_table(stock_info_df, self.output, partition_columns=["partition_date"])

        logging.info(f"Saved to {self.output}")

