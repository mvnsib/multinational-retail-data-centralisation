-- task 1

SELECT country_code, COUNT(country_code) AS total_no_stores
FROM dim_store_details
WHERE country_code IS NOT NULL
GROUP BY country_code
ORDER BY total_no_stores DESC;


-- task 2

SELECT locality, COUNT(*) AS total_no_stores
FROM dim_store_details
GROUP BY locality
ORDER BY total_no_stores DESC
limit 7;


-- task 3

SELECT ROUND(SUM(ot.product_quantity*dp.product_price)::numeric,2) AS total_revenue,ddt.month
FROM orders_table ot
JOIN dim_date_times ddt ON  ot.date_uuid = ddt.date_uuid
JOIN dim_products dp ON  ot.product_code = dp.product_code
GROUP BY ddt.month
ORDER BY SUM(ot.product_quantity*dp.product_price) DESC;


-- task 4

SELECT 
COUNT(ot.product_quantity) AS number_of_sales,
SUM(ot.product_quantity) AS product_quantity_count,
CASE WHEN dsd.store_type = 'Web Portal' THEN 'Web'
ELSE 'Offline' END AS location
FROM orders_table ot
JOIN dim_store_details dsd ON ot.store_code = dsd.store_code
GROUP BY location
ORDER BY product_quantity_count ASC;


-- task 5

SELECT dsd.store_type,
ROUND(SUM (ot.product_quantity*dp.product_price)::numeric, 2) AS total_sales,
ROUND((100 * SUM(ot.product_quantity * dp.product_price) / SUM(SUM(ot.product_quantity * dp.product_price)) OVER())::numeric, 2) AS percentage_total 
FROM orders_table ot
JOIN dim_store_details dsd ON ot.store_code = dsd.store_code
JOIN dim_products dp ON ot.product_code = dp.product_code
JOIN dim_date_times ddt ON ot.date_uuid = ddt.date_uuid
GROUP BY dsd.store_type
ORDER BY percentage_total DESC;


-- task 6

SELECT
ROUND(SUM(ot.product_quantity * dp.product_price)::numeric, 2) AS total_sales,
ddt.year AS year,
ddt.month AS month
FROM orders_table ot
JOIN dim_date_times ddt ON ot.date_uuid = ddt.date_uuid
JOIN dim_products dp ON ot.product_code = dp.product_code
GROUP BY year, month
ORDER BY total_sales DESC
LIMIT 10;


-- task 7

SELECT SUM(dsd.staff_numbers) AS total_staff_numbers, dsd.country_code
FROM dim_store_details dsd
WHERE dsd.country_code IS NOT NULL
GROUP BY dsd.country_code
ORDER BY total_staff_numbers DESC;


-- task 8

SELECT ROUND(SUM (ot.product_quantity*dp.product_price)::numeric, 2) AS total_sales,
dsd.store_type, dsd.country_code
FROM orders_table ot
JOIN dim_products dp ON ot.product_code = dp.product_code
JOIN dim_store_details dsd ON ot.store_code = dsd.store_code
WHERE dsd.country_code = 'DE'
GROUP BY dsd.store_type, dsd.country_code
ORDER BY total_sales ASC;


-- task 9

WITH cte_date_time(date_uuid, year, month, day, hour, minutes, seconds) as (
		SELECT date_uuid,year, month, day,
		EXTRACT(hour FROM timestamp::time) AS hour,
		EXTRACT(minute FROM timestamp::time) AS minutes,
		EXTRACT(second FROM timestamp::time) AS seconds
		FROM dim_date_times),

	
	cte_timestamp(timestamp, date_uuid, year) AS (
		SELECT MAKE_TIMESTAMP(dt.year::INT, 
							  dt.month::INT,
							  dt.day::INT,
							  dt.hour::INT,
							  dt.minutes::INT,
							  dt.seconds::FLOAT
							  ),
				dt.date_uuid,
				dt.year
		FROM cte_date_time dt
	),
	

	cte_time_diff(year, cte_timestamp) AS (
		SELECT ts.year, LEAD(ts.timestamp) OVER (ORDER BY ts.timestamp ASC) - ts.timestamp AS time_diff
		FROM orders_table
		LEFT JOIN cte_timestamp ts ON orders_table.date_uuid = ts.date_uuid
	),
	
	
	year_diffs(year, avg_timestamp_diff) AS (
		SELECT year, AVG(cte_timestamp) AS avg_timestamp_diff
		FROM cte_time_diff
		GROUP BY year
		ORDER BY avg_timestamp_diff DESC)
		
SELECT 
	year, 
	CONCAT('hours:', EXTRACT(HOUR FROM avg_timestamp_diff), '  ',
					'minutes:', EXTRACT(MINUTE FROM avg_timestamp_diff),'  ',
				   'seconds:', ROUND(EXTRACT(SECOND FROM avg_timestamp_diff)),'  ',
				   'milliseconds:', ROUND(EXTRACT(MILLISECOND FROM avg_timestamp_diff))) AS actual_time_taken
FROM year_diffs
LIMIT 5;
	
	
		
	


