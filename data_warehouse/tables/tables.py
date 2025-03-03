from data_stack.models.data_asset.table.table import OdsTable, DwdTable, Database, Catalog, TableEngine

ods_stock_market_s_d = OdsTable("ods_stock_market_s_d", database=Database.ODS, catalog=Catalog.ICEBERG_CATALOG, engine=TableEngine.ICEBERG)
ods_stock_info_s_d = OdsTable("ods_stock_info_s_d", database=Database.ODS, catalog=Catalog.ICEBERG_CATALOG, engine=TableEngine.ICEBERG)
dwd_stock_market_s_d = DwdTable("dwd_stock_market_s_d", database=Database.DWD, catalog=Catalog.ICEBERG_CATALOG, engine=TableEngine.ICEBERG)
