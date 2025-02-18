import logging

import akshare
import pandas as pd


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

        return df

    except Exception as e:
        logging.error(f"Error while fetching stock data for {stock_code}: {str(e)}")
        return None
