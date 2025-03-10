import logging

from pyspark.sql.functions import expr

from data_stack.governance.quality import DataQualityRule
from data_stack.models.data_asset.table.table import OdsTable, Database, Catalog, TableEngine, TableSchema, TableField
from data_stack.models.job.base_job import Job

ods_stock_info_s_d = OdsTable(
    "ods_stock_info_s_d",
    database=Database.ODS,
    catalog=Catalog.ICEBERG_CATALOG,
    engine=TableEngine.ICEBERG,
    schema=TableSchema(
        fields=[
            TableField("stock_exchange", "STRING", "证券交易所", [DataQualityRule.NOT_NULL]),
            TableField("stock_code", "STRING", "股票代码", [DataQualityRule.NOT_NULL, DataQualityRule.UNIQUE]),
            TableField("stock_name", "STRING", "股票名称", [DataQualityRule.NOT_NULL]),
            TableField("company_name", "STRING", "公司名称", [DataQualityRule.NOT_NULL]),
            TableField("industry", "STRING", "所属行业", [DataQualityRule.NOT_NULL]),
            TableField("listing_date", "STRING", "上市日期", [DataQualityRule.NOT_NULL]),
            TableField("ingest_time", "TIMESTAMP", "采集时间", [DataQualityRule.NOT_NULL]),
        ],
        partition_fields=[
            "partition_date"
        ]

    )
)


class OdsStockInfoSDJob(Job):
    """
    ODS Stock Info Snapshot Daily job
    """
    name = "ods_stock_info_s_d"

    inputs = []
    output = ods_stock_info_s_d

    def process(self):
        from data_warehouse.services import stock_service

        stock_info_pd_df = stock_service.get_all_stock_list()
        stock_info_df = self.spark.createDataFrame(stock_info_pd_df)

        from data_stack.utils import dataframe_writer
        stock_info_df = stock_info_df.withColumn("partition_date", expr("TO_DATE(ingest_time)"))
        dataframe_writer.write_to_table(stock_info_df, self.output, partition_columns=["partition_date"])

        logging.info(f"Saved to {self.output}")

