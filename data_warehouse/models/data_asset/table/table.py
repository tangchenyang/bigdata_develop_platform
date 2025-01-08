from data_warehouse.models.data_asset.asset_type import AssetType
from data_warehouse.models.data_asset.base_data_asset import DataAsset
from data_warehouse.models.data_asset.table.table_type import TableType


class Table(DataAsset):
    asset_type = AssetType.TABLE

    def __init__(self,
                 name: str,
                 database: str = None,
                 catalog: str = None,
                 schema=None,
                 engine: str = "spark",
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

    def __str__(self):
        return f"{self.name} ({self.database})"


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
