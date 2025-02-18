import logging

import akshare
import pandas as pd


def get_fund_info(fund_code: str) -> pd.DataFrame:
    """
    :param fund_code:
    :return: pd.DataFrame
    """
    try:
        df = akshare.fund_open_fund_info_em(symbol=fund_code, indicator="单位净值走势", period="成立来")

        if df.empty:
            logging.warning(f"Not found any data for fund {fund_code} ")
            return None

        df['fund_code'] = fund_code

        return df

    except Exception as e:
        logging.error(f"Error while fetching fund data for {fund_code}: {str(e)}")
        return None
