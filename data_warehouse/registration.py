from data_stack.meta import job_meta, data_meta
from data_warehouse.jobs.dwd.dwd_stock_market_s_d import DwdStockMarketSD
from data_warehouse.jobs.ods.ods_stock_market_s_d import OdsStockMarketSD
from data_warehouse.jobs.ods.ods_stock_info_s_d import OdsStockInfoSD
from data_warehouse.tables import tables

jobs = [
    OdsStockMarketSD(),
    DwdStockMarketSD(),
    OdsStockInfoSD()
]

data_assets = [
    tables.ods_stock_market_s_d,
    tables.dwd_stock_market_s_d,
    tables.ods_stock_info_s_d,
]


def register_jobs():
    job_meta.register_jobs(jobs)


def register_data_assets():
    data_meta.register_data_assets(data_assets)


def register_all():
    register_data_assets()
    register_jobs()
