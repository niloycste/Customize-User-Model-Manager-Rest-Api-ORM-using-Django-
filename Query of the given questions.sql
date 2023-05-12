SELECT * FROM shop.sales_data;

/*
Q1: Total number of orders count per year
*/

SELECT EXTRACT(YEAR FROM order_date) AS year, COUNT(*) AS order_count
FROM sales_data
GROUP BY year
ORDER BY year;
/*
Q2: Total count of distinct customers
*/
SELECT COUNT(DISTINCT customer_id) AS total_distinct_customers
FROM sales_data;

/*
Q3: Top 3 customers who have ordered the most with their total amount of
transactions.
*/
SELECT customer_id, customer_name, SUM(sales) AS total_amount
FROM sales_data
GROUP BY customer_id, customer_name
ORDER BY total_amount DESC
LIMIT 3;

/*
Q4: Customer Transactions per Year (from the beginning year to last year)
*/
SELECT EXTRACT(YEAR FROM order_date) AS year, COUNT(*) AS transaction_count
FROM sales_data
GROUP BY year
ORDER BY year;
/*
Q5: Most selling items sub-category names
*/
SELECT sub_category, SUM(sales) AS total_sales
FROM sales_data
GROUP BY sub_category
ORDER BY total_sales DESC
LIMIT 1;
/*
Q6: Region basis sales performance PIE CHART
*/
SELECT region, SUM(sales) AS total_sales
FROM sales_data
GROUP BY region
ORDER BY total_sales DESC;

/*
Q7: Sales performance LINE CHART over the years
*/
SELECT EXTRACT(YEAR FROM order_date) AS year, SUM(sales) AS total_sales
FROM sales_data
GROUP BY year
ORDER BY year;









