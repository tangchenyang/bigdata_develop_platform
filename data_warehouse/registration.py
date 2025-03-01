from data_stack.meta import job_meta, data_meta
from data_warehouse.jobs.dwd.dwd_stock_market_snapshot_daily import DwdStockMarketSnapshotDaily
from data_warehouse.jobs.ods.ods_stock_market_snapshot_daily import OdsStockMarketSnapshotDaily
from data_warehouse.jobs.ods.ods_stock_info_full_daily import OdsStockInfoFullDaily
from data_warehouse.tables import tables

jobs = [
    OdsStockMarketSnapshotDaily(),
    DwdStockMarketSnapshotDaily(),
    OdsStockInfoFullDaily()
]

data_assets = [
    tables.ods_stock_market_snapshot_daily,
    tables.dwd_stock_marketa_snapshot_daily,
    tables.ods_stock_info_full_daily,
]


def register_jobs():
    job_meta.register_jobs(jobs)


def register_data_assets():
    data_meta.register_data_assets(data_assets)


def register_all():
    register_data_assets()
    register_jobs()
