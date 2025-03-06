import logging
from datetime import date
from typing import Dict

from pyspark.sql import SparkSession
from pyspark.sql.functions import count_if, count, lit, count_distinct, col, collect_set, max as f_max

from data_stack.governance.quality.quality_type import QualityType
from data_stack.models.data_asset.base_data_asset import DataAsset
from data_stack.models.data_asset.file.file import File
from data_stack.models.data_asset.table.table import Table


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
                if rule == "Not Null":
                    select_expr.append(count_if(table_df[field.name].isNull()).cast("string").alias(f"{field.name}_isnull_rows"))
                elif rule == "Unique":
                    select_expr.append(
                        (count_distinct(table_df[field.name]).alias(f"{field.name}_isnull_count") == count(lit(1))).cast("string").alias(f"{field.name}_is_unique")
                    )
                else:
                    raise Exception(f"Unsupported rule {rule}")

        check_result_df = table_df.select(*select_expr)

        id_columns = ["catalog", "database", "table", "partition_date"]
        rest_columns = [c for c in check_result_df.columns if c not in id_columns]

        check_result_df.unpivot(ids=id_columns, values=rest_columns, variableColumnName="metric_name", valueColumnName="metric_value").show(100,
                                                                                                                                            False)
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
