from data_stack.models.data_asset.table.table import TableSchema, TableField, Database, Catalog, TableEngine, DimTable
from data_stack.models.job.base_job import Job
from data_warehouse.layers.ods.ods_stock_info_s_d import ods_stock_info_s_d

dim_stock_schema = TableSchema(
    fields=[
        TableField("stock_code", "STRING", "股票代码", ["not_null", "unique"]),
        TableField("stock_name", "STRING", "股票名称", ["not_null"]),
        TableField("stock_exchange", "STRING", "证券交易所", ["not_null"]),
        TableField("company_name", "STRING", "公司名称", ["not_null"]),
        TableField("industry", "STRING", "所属行业", ["not_null"]),
        TableField("listing_date", "STRING", "上市日期", ["not_null"])
    ]
)
dim_stock = DimTable(
    "dim_stock",
    database=Database.DIM,
    catalog=Catalog.ICEBERG_CATALOG,
    engine=TableEngine.ICEBERG,
    schema=dim_stock_schema
)


class DimStockJob(Job):
    """
    Dim Stock
    """
    name = "dim_stock"

    inputs = [ods_stock_info_s_d]
    output = dim_stock

    def process(self):
        from data_stack.utils import dataframe_reader
        ods_df = dataframe_reader.read_from_table(self.inputs[0], self.spark)

        dim_df = ods_df.drop("ingest_time")

        from data_stack.utils import dataframe_writer
        dataframe_writer.write_to_table(dim_df, self.output)
