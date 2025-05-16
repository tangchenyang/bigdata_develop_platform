import logging

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, max as f_max

from data_stack.models.data_asset.table.table import Table, TableEngine


def read_from_table(table: Table, spark: SparkSession) -> DataFrame:
    table_full_name = table.full_name()
    logging.info(f"Reading from {table_full_name}")
    table_df = spark.read.table(table_full_name)

    if table.schema.partition_fields and "partition_date" in table.schema.partition_fields:
        latest_partition_date = table_df.select(f_max(col("partition_date"))).collect()[0][0]
        table_df = table_df.filter(col("partition_date") == latest_partition_date)
    return table_df
