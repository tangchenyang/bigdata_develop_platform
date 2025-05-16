from data_stack.meta import job_meta, data_meta
from data_warehouse.layers.ads.ads_stock_boundary_s_d import AdsStockBoundarySDJob, ads_stock_boundary_s_d
from data_warehouse.layers.dim.dim_stock import DimStockJob, dim_stock
from data_warehouse.layers.dwd.dwd_stock_market_s_d import DwdStockMarketSDJob, dwd_stock_market_s_d
from data_warehouse.layers.dws.dws_stock_market_s_d import DwsStockMarketSDJob, dws_stock_market_s_d
from data_warehouse.layers.ods.ods_stock_info_s_d import OdsStockInfoSDJob, ods_stock_info_s_d
from data_warehouse.layers.ods.ods_stock_market_s_d import OdsStockMarketSDJob, ods_stock_market_s_d

jobs = [
    OdsStockMarketSDJob(),
    DwdStockMarketSDJob(),
    OdsStockInfoSDJob(),
    DimStockJob(),
    DwsStockMarketSDJob(),
    AdsStockBoundarySDJob(),
]

data_assets = [
    ods_stock_market_s_d,
    dwd_stock_market_s_d,
    ods_stock_info_s_d,
    dim_stock,
    dws_stock_market_s_d,
    ads_stock_boundary_s_d,
]


def register_jobs():
    job_meta.register_jobs(jobs)


def register_data_assets():
    data_meta.register_data_assets(data_assets)


def register_all():
    register_data_assets()
    register_jobs()
