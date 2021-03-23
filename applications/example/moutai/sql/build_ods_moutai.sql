create database if not exists example;

-- create ods.moutai
drop table if exists example.ods_moutai;
create table example.ods_moutai(
    trade_date          string  comment "日期",
    opening             string  comment "开盘",
    highest             string  comment "最高",
    lowest              string  comment "最低",
    closing             string  comment "收盘",
    trading_volume      string  comment "成交金额",
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

load data local inpath '/root/bigdata_develop_platform/applications/example/moutai/data/moutai.csv' overwrite into table example.ods_moutai;