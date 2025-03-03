import logging
from typing import Dict

from pyspark.sql import SparkSession
from pyspark.sql.functions import count_if, count, lit

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
        table_df.cache()
        select_expr = [count(lit(1)).alias("total_rows")]
        table_quality = QualityType.BRONZE.value
        for field in table.schema.fields:
            for rule in field.rules:
                if rule == "Not Null":
                    select_expr.append(count_if(table_df[field.name].isNull()).alias(f"{field.name}_isnull_rows"))
                elif rule == "Unique":
                    # select_expr.append(count_if(table_df[field.name].isNull()).alias(f"{field.name}_isnull_count"))
                    pass
        table_df.select(*select_expr).show(1000, False)
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
