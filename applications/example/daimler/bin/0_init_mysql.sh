mysql --connect-expired-password -uroot -p123456 <<EOF
DROP DATABASE IF EXISTS daimler;
CREATE DATABASE daimler;
USE daimler;
CREATE TABLE IF NOT EXISTS deal_record
(
    record_id           TEXT,
    dealer_id           TEXT,
    deal_total_price    DOUBLE,
    deal_time           TIMESTAMP

);
INSERT INTO deal_record VALUES('R0001', 'D0001', 100, '2021-06-01 10:10:10');
INSERT INTO deal_record VALUES('R0002', 'D0001', 200, '2021-06-02 10:10:10');
INSERT INTO deal_record VALUES('R0003', 'D0002', 50, '2021-06-03 10:10:10');
INSERT INTO deal_record VALUES('R0004', 'D0002', 50, '2021-06-04 10:10:10');

CREATE TABLE IF NOT EXISTS deal_item_list
(
    record_id           TEXT,
    item_id             TEXT,
    item_name           TEXT,
    item_price          DOUBLE,
    item_number         DOUBLE
);
INSERT INTO deal_item_list VALUES('R0001', 'I0001', 'milk', 50, 1.0);
INSERT INTO deal_item_list VALUES('R0001', 'I0002', 'apple', 5, 10.0);
INSERT INTO deal_item_list VALUES('R0002', 'I0001', 'cake', 10, 1.0);
INSERT INTO deal_item_list VALUES('R0002', 'I0003', 'rio', 15, 2.0);
INSERT INTO deal_item_list VALUES('R0002', 'I0004', 'banana', 2, 5.0);
INSERT INTO deal_item_list VALUES('R0002', 'I0005', 'milk', 50, 1.0);
INSERT INTO deal_item_list VALUES('R0003', 'I0001', 'beer', 5, 6.0);
INSERT INTO deal_item_list VALUES('R0003', 'I0002', 'peanut', 5, 4.0);
INSERT INTO deal_item_list VALUES('R0004', 'I0001', 'beer', 5, 6.0);
INSERT INTO deal_item_list VALUES('R0004', 'I0002', 'peanut', 5, 4.0);


CREATE TABLE IF NOT EXISTS dw_dim_dealer
(
    dealer_id               text,
    dealer_name             text,
    dealer_gender           text
);
INSERT INTO dw_dim_dealer VALUES('D0001', 'Miss Lee', 'female');
INSERT INTO dw_dim_dealer VALUES('D0002', 'Mr. Wang', 'male');


DROP DATABASE IF EXISTS dw;
CREATE DATABASE dw;
USE dw;

CREATE TABLE IF NOT EXISTS DW_DM_SALES_TOP1_ITEM_ON_DEALER
(
  dealer_name    TEXT,
  item_name      TEXT,
  sale_volume    DOUBLE
);
EOF