import logging

from pyspark.sql import DataFrame

from data_stack.models.data_asset.table.table import Table, TableEngine


def write_to_table(df, table: Table, partition_columns: list[str] =None):
    if table.engine == TableEngine.ICEBERG:
        write_to_iceberg_table(df, table, partition_columns=partition_columns)
    # elif table.engine == TableEngine.SPARK:
    #     pass
    else:
        raise ValueError(f"Unsupported table engine: {table.engine}")


def write_to_iceberg_table(df: DataFrame, table: Table, partition_columns: list[str]=None):
    _spark = df.sparkSession
    # todo validate schema between dataframe and schema in table
    table_full_name = table.full_name()

    writer = df.writeTo(table_full_name)

    if partition_columns:
        partitioned_by_cols = partition_columns if isinstance(partition_columns, list) else [partition_columns]
        writer = writer.partitionedBy(*partitioned_by_cols)

    if not _spark.catalog.tableExists(table_full_name):
        logging.info(f"Table {table_full_name} doesn't exist, creating it.")
        writer.create()
    else:
        logging.info(f"Write to {table_full_name} with overwritePartitions.")
        writer.overwritePartitions() # todo support more mode
        logging.info(f"Write to {table_full_name} successfully.")

