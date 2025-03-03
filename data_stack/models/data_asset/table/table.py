import logging

from data_stack.models.data_asset.asset_type import AssetType
from data_stack.models.data_asset.base_data_asset import DataAsset
from data_stack.models.data_asset.table.table_type import TableType
from data_stack.sugar import EnumSugar


class TableEngine(EnumSugar):
    SPARK = "spark"
    ICEBERG = "iceberg"

class Catalog(EnumSugar):
    SPARK_CATALOG = "spark_catalog"
    ICEBERG_CATALOG = "iceberg_catalog"

class Database(EnumSugar):
    DEFAULT = "default"
    ODS = "ods"
    DWD = "dwd"
    DIM = "dim"
    ADS = "ads"


class FieldType(EnumSugar):
    STRING = "string"


class TableField:
    def __init__(self, name: str, type: str, comment: str = None, rules: list[str] = None):
        self.name = name
        self.type = type
        self.comment = comment
        self.rules = rules


class TableSchema:
    def __init__(self, fields: list[TableField] = None, partition_fields: list[str] = None):
        self.fields = fields
        self.partition_fields = partition_fields

    def columns(self):
        """
        Return a list of column names
        """
        return [field.name for field in self.fields]

class Table(DataAsset):
    asset_type = AssetType.TABLE

    def __init__(self,
                 name: str,
                 database: Database = Database.DEFAULT,
                 catalog: Catalog = Catalog.SPARK_CATALOG,
                 schema: TableSchema = None,
                 engine: TableEngine = TableEngine.SPARK,
                 **kwargs,
                 ):
        """

        :param name:
        :param database:
        :param catalog:
        :param engine:
        :param schema:
        :param kwargs:
        """

        super().__init__(name, **kwargs)

        self.database = database
        self.catalog = catalog
        self.schema = schema
        self.engine = engine

        self.validate_table_name()

        assert self.name is not None, "Table name must be provided"
        assert self.schema is not None, "Table schema must be provided"
        assert self.engine is not None, "Table engine must be provided"


    def full_name(self):
        table_name_sections = [self.catalog.value, self.database.value, self.name]
        table_name_sections = [section for section in table_name_sections if section]
        return ".".join(table_name_sections)

    def validate_table_name(self):
        """todo
        Follow the table naming convention:
        <>_<>_<>_<period>
        ods_stock_full_daily
        :return:
        """
        logging.info(f"Validating table name: {self.name}")
        full_name = self.full_name()
        pass


class OdsTable(Table):
    table_type = TableType.ODS


class DimTable(Table):
    table_type = TableType.DIM


class DwdTable(Table):
    table_type = TableType.DWD


class DwsTable(Table):
    table_type = TableType.DWS


class AdsTable(Table):
    table_type = TableType.ADS
