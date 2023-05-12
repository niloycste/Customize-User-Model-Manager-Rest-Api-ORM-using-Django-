create database shop;
show variables like "secure_file_priv";
create table  sales_data(
id bigint,
    order_id text,
    order_date date,
    ship_date date,
    ship_mode text,
    customer_id text,
    customer_name text,
    segment text,
    country text,
    city text,
    state text,
    postal_code text,
    region text,
    product_id text,
    category text,
    sub_category text,
    product_name text,
    sales numeric(10,2)
 );
 
 LOAD DATA  INFILE "C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\sales_data.csv"
INTO TABLE sales_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES; 

select * from sales_data;