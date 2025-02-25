import logging

from data_stack.models.job.base_job import Job
from data_warehouse.tables import tables


class DwdStockDaily(Job):
    name = "dwd_stock_daily"

    inputs = [
        tables.ods_stock_daily
    ]
    output = tables.dwd_stock_daily

    def process(self):
        logging.info(f"Reading from {self.inputs}")
        ods_df = self.spark.read.table(self.inputs[0].full_name())
        logging.info(f"Transforming")

        dwd_df = ods_df

        from data_stack.utils import dataframe_writer
        dataframe_writer.write_to_table(dwd_df, self.output, partition_columns=["stock_code"])

        logging.info(f"Saved to {self.output}")

