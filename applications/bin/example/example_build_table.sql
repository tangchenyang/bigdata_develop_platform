create database if not exists ods;

-- create ods.example_moutai
drop table if exists ods.example_moutai;
create table ods.example_moutai(
    trade_date          string  comment "日期",
    opening             string  comment "开盘",
    highest             string  comment "最高",
    lowest              string  comment "最低",
    closing             string  comment "收盘",
    trading_volume      string  comment "成交量",
    trading_amount      string  comment "成交金额",
    up_down_amount      string  comment "涨跌金额",
    up_down_ratio       string  comment "涨跌比例",
    contraction         string  comment "缩",
    high_low_ratio      string  comment "高低差比例",
    SH_Shanghai         string  comment "SH上证",
    SH                  string  comment "sh"
)
row format delimited fields terminated by '|'
lines terminated by '\n'
stored as textfile;

-- load data
load data local inpath '${hivevar:app_home}/bin/example/example_moutai.csv' into table ods.example_moutai;

-- select data
select * from ods.example_moutai limit 20;