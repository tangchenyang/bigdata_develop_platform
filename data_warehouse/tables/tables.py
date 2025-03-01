from data_stack.models.data_asset.table.table import OdsTable, DwdTable, Database, Catalog, TableEngine

ods_stock_market_snapshot_daily = OdsTable("ods_stock_market_snapshot_daily", database=Database.ODS, catalog=Catalog.ICEBERG_CATALOG, engine=TableEngine.ICEBERG)
ods_stock_info_full_daily = OdsTable("ods_stock_info_full_daily", database=Database.ODS, catalog=Catalog.ICEBERG_CATALOG, engine=TableEngine.ICEBERG)
dwd_stock_marketa_snapshot_daily = DwdTable("dwd_stock_market_snapshot_daily", database=Database.DWD, catalog=Catalog.ICEBERG_CATALOG, engine=TableEngine.ICEBERG)
