import logging
from datetime import date
from typing import Dict

from pyspark.sql import SparkSession
from pyspark.sql.functions import count_if, count, lit, count_distinct, col, max as f_max, when, nvl

from data_stack.governance.quality import QualityType, DataQualityRule
from data_stack.models.data_asset.base_data_asset import DataAsset
from data_stack.models.data_asset.file.file import File
from data_stack.models.data_asset.table.table import Table, SysTable, Database, Catalog, TableSchema, TableField, TableEngine


class QualityChecker:

    # todo save to table or some where
    _data_asset_qualities: Dict[str, QualityType] = {}

    def __init__(self, spark: SparkSession):
        self.spark = spark

    def check(self, data_asset: DataAsset):
        if isinstance(data_asset, Table):
            checker = TableQualityChecker(self.spark)
        elif isinstance(data_asset, File):
            checker = FileQualityChecker(self.spark)
        else:
            raise Exception(f"Unsupported data set {data_asset}")

        checker.check(data_asset)


    @staticmethod
    def store_qualities(data_asset_name: str, data_asset_quality: QualityType):
        """
        :param data_asset_name:
        :param data_asset_quality:
        :return:
        """
        QualityChecker._data_asset_qualities[data_asset_name] = data_asset_quality

    @staticmethod
    def get_all_qualities():
        return QualityChecker._data_asset_qualities

class TableQualityChecker(QualityChecker):
    data_stack_table_quality_detail = SysTable(
        name="data_stack_table_quality_detail",
        database=Database.SYS,
        catalog=Catalog.ICEBERG_CATALOG,
        schema=TableSchema([
            TableField(name="catalog", type="STRING", comment=""),
            TableField(name="database", type="STRING", comment=""),
            TableField(name="table", type="STRING", comment=""),
            TableField(name="partition_date", type="STRING", comment=""),
            TableField(name="metric_name", type="STRING", comment=""),
            TableField(name="metric_value", type="STRING", comment=""),
        ]),
        engine=TableEngine.ICEBERG
    )

    data_stack_table_quality_summary = SysTable(
        name="data_stack_table_quality_summary",
        database=Database.SYS,
        catalog=Catalog.ICEBERG_CATALOG,
        schema=TableSchema([
            TableField(name="catalog", type="STRING", comment=""),
            TableField(name="database", type="STRING", comment=""),
            TableField(name="table", type="STRING", comment=""),
            TableField(name="partition_date", type="STRING", comment=""),
            TableField(name="quality_type", type="STRING", comment="")
        ]),
        engine=TableEngine.ICEBERG
    )

    def check(self, table: Table):
        """
        todo check the quality of the table based on the inputs and the table itself
        :param table:
        :return:
        """
        table_df = self.spark.table(table.full_name()) # todo consider incremental check
        select_expr = [
            lit(table.catalog.value).alias("catalog"),
            lit(table.database.value).alias("database"),
            lit(table.name).alias("table"),
            count(lit(1)).cast("string").alias("total_rows")
        ]
        if table.schema.partition_fields and "partition_date" in table.schema.partition_fields:
            current_date = date.today().strftime("%Y-%m-%d")  # todo consider pass from execution params
            table_df = table_df.filter(col("partition_date") == current_date)
            select_expr.append(f_max("partition_date").cast("string").alias("partition_date"))

        table_df.cache()

        table_quality = QualityType.BRONZE.value
        for field in table.schema.fields:
            for rule in field.rules:
                metric_name = f"{field.name}_{rule.value}"
                if rule == DataQualityRule.NOT_NULL:
                    select_expr.append(count_if(nvl(table_df[field.name], lit("")) == lit("")).cast("string").alias(metric_name))
                elif rule == DataQualityRule.UNIQUE:
                    select_expr.append(
                        (count_distinct(table_df[field.name]) == count(lit(1))).cast("string").alias(metric_name)
                    )
                else:
                    raise Exception(f"Unsupported rule {rule.value}")

        check_result_df = table_df.select(*select_expr)

        id_columns = ["catalog", "database", "table", "partition_date"]
        rest_columns = [c for c in check_result_df.columns if c not in id_columns]

        table_quality_detail = check_result_df.unpivot(
            ids=id_columns, values=rest_columns, variableColumnName="metric_name", valueColumnName="metric_value"
        )  # todo try to support Drill-Down for each metric
        from data_stack.utils import dataframe_writer
        dataframe_writer.write_to_table(table_quality_detail, self.data_stack_table_quality_detail, partition_columns=["partition_date", "table"])

        table_quality_summary = (
            table_quality_detail
            .groupby("catalog", "database", "table", "partition_date")
            .agg(
                (count_if((col("metric_name") == "total_rows") & (col("metric_value") == "0")) == 0).alias("table_not_empty"),
                (count_if(col("metric_name").like("%_isnull_count") & (col("metric_value") != "0")) == 0).alias("not_null_passed"),
                (count_if(col("metric_name").like("%_is_unique") & (col("metric_value") != "true")) == 0).alias("unique_passed")
            )
            .withColumn(
                "quality_type",
                when(col("table_not_empty") & col("not_null_passed") & col("unique_passed"), lit(QualityType.GOLD.value))
                .when(col("table_not_empty"), lit(QualityType.SILVER.value))
                .otherwise(lit(QualityType.BRONZE.value))
            )
            .drop("table_not_empty", "not_null_passed", "unique_passed")
        )

        dataframe_writer.write_to_table(table_quality_summary, self.data_stack_table_quality_summary, partition_columns=["partition_date", "table"])
        table_df.unpersist()

        QualityChecker._data_asset_qualities[table.name] = table_quality
        logging.info(f"Table {table.name}'s quality is {table_quality}")
        return None  # todo check more

class FileQualityChecker(QualityChecker):
    def check(self, file: File):
        """
        :param file:
        :return:
        """
        file_quality = QualityType.BRONZE.value
        QualityChecker._data_asset_qualities[file.name] = file_quality
        logging.info(f"File {file.name}'s quality is {file_quality}")
        return None  # todo check more
