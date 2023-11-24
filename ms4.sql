-- task 1

SELECT country_code, COUNT(country_code) AS total_no_stores
FROM dim_store_details
WHERE country_code IS NOT NULL
GROUP BY country_code
ORDER BY total_no_stores DESC;

-- task 2

SELECT locality, COUNT(locality) AS total_no_stores
FROM dim_store_details
GROUP BY locality
ORDER BY total_no_stores DESC
limit 7;

-- task 3

