import logging
from datetime import datetime

import akshare
import pandas as pd
import pytz


def get_stock_daily(stock_code: str, start_date: str = "19000101", end_date: str = "20990101") -> pd.DataFrame:
    """
    Get stock daily data
    :param self:
    :param stock_code: sh000001, with prefix sh: shanghai
    :param start_date:
    :param end_date:
    :return: pd.DataFrame
    """
    try:
        logging.info(f"Fetching stock data for {stock_code} from {start_date} to {end_date} ")

        df = akshare.stock_zh_a_daily(
            symbol=stock_code,
            start_date=start_date,
            end_date=end_date,
            adjust=""
        )

        if df.empty:
            logging.warning(f"Not found any data for stock {stock_code} in [{start_date}, {end_date}] ")
            return None
        df['stock_code'] = stock_code
        df['timestamp'] = datetime.now(tz=pytz.UTC)
        return df

    except Exception as e:
        logging.error(f"Error while fetching stock data for {stock_code}: {str(e)}")
        return None


def get_stock_list_sh():
    logging.info(f"Fetching stock list for Shanghai")
    stock_sh_a = akshare.stock_info_sh_name_code(symbol="主板A股")
    stock_sh_tech = akshare.stock_info_sh_name_code(symbol="科创板")

    stock_sh = pd.concat(objs=[stock_sh_a, stock_sh_tech], ignore_index=True)
    stock_sh["证券交易所"] = "上海证券交易所"
    stock_sh["所属行业"] = "UNKNOWN"

    stock_sh = stock_sh[["证券交易所", "证券代码", "证券简称", "公司全称", "所属行业", "上市日期"]]
    stock_sh.columns = ["证券交易所", "股票代码", "股票名称", "公司全称", "所属行业", "上市日期"]
    return stock_sh


def get_stock_list_sz():
    logging.info(f"Fetching stock list for Shenzhen")
    stock_sz = akshare.stock_info_sz_name_code(symbol="A股列表")
    stock_sz["A股代码"] = stock_sz["A股代码"].astype(str).str.zfill(6)

    stock_sz["证券交易所"] = "深圳证券交易所"
    stock_sz["公司全称"] = "UNKNOWN"
    stock_sz = stock_sz[["证券交易所", "A股代码", "A股简称", "公司全称", "所属行业", "A股上市日期"]]
    stock_sz.columns = ["证券交易所", "股票代码", "股票名称", "公司全称", "所属行业", "上市日期"]

    return stock_sz

def get_stock_list_bj():
    logging.info(f"Fetching stock list for Beijing")
    stock_bj = akshare.stock_info_bj_name_code()
    stock_bj["证券代码"] = stock_bj["证券代码"].astype(str).str.zfill(6)
    stock_bj["证券交易所"] = "北京证券交易所"
    stock_bj["公司全称"] = "UNKNOWN"

    stock_bj = stock_bj[["证券交易所", "证券代码", "证券简称", "公司全称", "所属行业", "上市日期"]]
    stock_bj.columns = ["证券交易所", "股票代码", "股票名称", "公司全称", "所属行业", "上市日期"]
    return stock_bj


def get_all_stock_list():
    logging.info(f"Fetching all stock list")

    stock_sh = get_stock_list_sh()
    stock_sz = get_stock_list_sz()
    stock_bj = get_stock_list_bj()

    all_stock = pd.concat(objs=[stock_sh, stock_sz, stock_bj], ignore_index=True)
    all_stock['timestamp'] = datetime.now(tz=pytz.UTC)
    all_stock.columns = ["stock_exchange", "stock_code", "stock_name", "company_name", "industry", "listing_date", "timestamp"]
    return all_stock

