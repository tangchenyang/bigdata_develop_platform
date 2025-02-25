from data_stack.meta import job_meta, data_meta
from data_warehouse.jobs.dwd_stock_daily import DwdStockDaily
from data_warehouse.jobs.ods.ods_stock_daily import OdsStockDaily
from data_warehouse.tables import tables

jobs = [
    OdsStockDaily(),
    DwdStockDaily(),
]

data_assets = [
    tables.ods_stock_daily,
    tables.dwd_stock_daily,
]


def register_jobs():
    job_meta.register_jobs(jobs)


def register_data_assets():
    data_meta.register_data_assets(data_assets)


def register_all():
    register_data_assets()
    register_jobs()
