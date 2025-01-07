from data_warehouse.models.data_asset.asset_type import AssetType
from data_warehouse.models.data_asset.data_asset import DataAsset
from data_warehouse.models.data_asset.table.table_type import TableType


class Table(DataAsset):
    asset_type = AssetType.TABLE

    def __init__(self,
                 table_name: str,
                 database_name: str = None,
                 catalog_name: str = None,
                 schema=None,
                 engine: str = "spark",
                 **kwargs,
                 ):
        """

        :param table_name:
        :param database_name:
        :param catalog_name:
        :param engine:
        :param schema:
        :param kwargs:
        """

        super().__init__(**kwargs)

        self.table_name = table_name
        self.database_name = database_name
        self.catalog_name = catalog_name
        self.schema = schema
        self.engine = engine

    def __str__(self):
        return f"{self.table_name} ({self.database_name})"


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
