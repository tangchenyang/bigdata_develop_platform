from data_stack.meta import job_meta, data_meta
from data_stack.models.data_asset.table.table import OdsTable, DwdTable
from data_warehouse.jobs.dwd_moutai import DwdMoutai

jobs = [
    DwdMoutai(),
]

data_assets = [
    OdsTable("ods_moutai"),
    DwdTable("dwd_moutai"),
]


def register_jobs():
    job_meta.register_jobs(jobs)


def register_data_assets():
    data_meta.register_data_assets(data_assets)


def register_all():
    register_data_assets()
    register_jobs()
