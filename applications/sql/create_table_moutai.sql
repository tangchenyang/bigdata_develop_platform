create table ods.moutai(
    trade_date          string  commit "日期",
    opening             string  commit "开盘",
    highest             string  commit "最高",
    lowest              string  commit "最低",
    closing             string  commit "收盘",
    trading_volume      string  commit "成交金额",
    up_down_amount      string  commit "涨跌金额",
    up_down_ratio       string  commit "涨跌比例",
    contraction         string  commit "缩",
    high_low_ratio      string  commit "高低差比例",
    SH_Shanghai         string  commit "SH上证",
    SH                  string  commit "sh"
);