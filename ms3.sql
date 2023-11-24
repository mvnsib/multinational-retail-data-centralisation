-- task 1
SELECT MAX(LENGTH(CAST(card_number AS TEXT)))
FROM orders_table
GROUP BY card_number
ORDER BY MAX(LENGTH(CAST(card_number AS TEXT))) DESC
LIMIT 1;

SELECT MAX(LENGTH(CAST(store_code AS TEXT)))
FROM orders_table
GROUP BY store_code
ORDER BY MAX(LENGTH(CAST(store_code AS TEXT))) DESC
LIMIT 1;

SELECT MAX(LENGTH(CAST(product_code AS TEXT)))
FROM orders_table
GROUP BY product_code
ORDER BY MAX(LENGTH(CAST(product_code AS TEXT))) DESC
LIMIT 1;

ALTER TABLE orders_table
ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID,
ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID,
ALTER COLUMN card_number TYPE VARCHAR(19),
ALTER COLUMN store_code TYPE VARCHAR(12),
ALTER COLUMN product_code TYPE VARCHAR(11),
ALTER COLUMN product_quantity TYPE SMALLINT;


-- task 2

SELECT MAX(LENGTH(CAST(country_code AS TEXT)))
FROM dim_user_table
GROUP BY country_code
ORDER BY MAX(LENGTH(CAST(country_code AS TEXT))) DESC
LIMIT 1; -- 3


ALTER TABLE dim_users
    ALTER COLUMN first_name TYPE VARCHAR(255),
    ALTER COLUMN last_name TYPE VARCHAR(255),
    ALTER COLUMN date_of_birth TYPE DATE,
    ALTER COLUMN country_code TYPE VARCHAR(3),
    ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID,
    ALTER COLUMN join_date TYPE DATE;


-- task 3


SELECT MAX(LENGTH(CAST(country_code AS TEXT)))
FROM dim_store_details
GROUP BY country_code
ORDER BY MAX(LENGTH(CAST(country_code AS TEXT))) DESC
LIMIT 1; -- 2


SELECT MAX(LENGTH(CAST(store_code AS TEXT)))
FROM dim_store_details
GROUP BY store_code
ORDER BY MAX(LENGTH(CAST(store_code AS TEXT))) DESC
LIMIT 1; -- 12


UPDATE dim_store_details 
SET
address = CASE WHEN address = NULL THEN 'N/A' ELSE address END,
latitude = CASE WHEN latitude = 'N/A' THEN NULL ELSE latitude END,
locality = CASE WHEN locality = NULL THEN 'N/A'ELSE locality END,
longitude = CASE WHEN longitude = 'N/A' THEN NULL ELSE longitude END;

UPDATE dim_store_details 
SET country_code = NULL WHERE store_type = 'Web Portal';

UPDATE dim_store_details 
SET continent = NULL WHERE store_type = 'Web Portal';


ALTER TABLE dim_store_details
ALTER COLUMN longitude TYPE FLOAT USING longitude::FLOAT,
ALTER COLUMN locality TYPE VARCHAR(255),
ALTER COLUMN store_code TYPE VARCHAR(12),
ALTER COLUMN staff_numbers TYPE SMALLINT USING staff_numbers::SMALLINT,
ALTER COLUMN opening_date TYPE DATE USING opening_date::DATE,
ALTER COLUMN store_type TYPE VARCHAR(255),
ALTER COLUMN latitude TYPE FLOAT USING latitude::FLOAT,
ALTER COLUMN country_code TYPE VARCHAR(2),
ALTER COLUMN continent TYPE VARCHAR(255);


-- task 4

UPDATE dim_products
SET product_price = REPLACE(product_price, '£', '');

ALTER TABLE dim_products
ADD COLUMN weight_class VARCHAR;

ALTER TABLE dim_products 
ALTER COLUMN weight TYPE FLOAT USING weight::FLOAT;


UPDATE dim_products
SET weight_class =
  CASE
    WHEN weight < 2 THEN 'Light'
    WHEN weight >= 2 AND weight < 40 THEN 'Mid_Sized'
    WHEN weight >= 40 AND weight < 140 THEN 'Heavy'
    WHEN weight >= 140 THEN 'Truck_Required'
    ELSE NULL
  END;


-- task 5

SELECT MAX(LENGTH(CAST("EAN" AS TEXT)))
FROM dim_products
GROUP BY "EAN"
ORDER BY MAX(LENGTH(CAST("EAN" AS TEXT))) DESC
LIMIT 1; -- 17

SELECT MAX(LENGTH(CAST(product_code AS TEXT)))
FROM dim_products
GROUP BY product_code
ORDER BY MAX(LENGTH(CAST(product_code AS TEXT))) DESC
LIMIT 1; -- 11

SELECT MAX(LENGTH(CAST(weight_class AS TEXT)))
FROM dim_products
GROUP BY weight_class
ORDER BY MAX(LENGTH(CAST(weight_class AS TEXT))) DESC
LIMIT 1; -- 14

ALTER TABLE dim_products 
RENAME COLUMN removed to still_available;

ALTER TABLE dim_products 
ALTER COLUMN product_price TYPE FLOAT USING product_price::FLOAT,
ALTER COLUMN weight TYPE FLOAT USING weight::FLOAT,
ALTER COLUMN "EAN" TYPE VARCHAR(17),
ALTER COLUMN product_code TYPE VARCHAR(11),
ALTER COLUMN date_added TYPE DATE USING date_added::DATE,
ALTER COLUMN uuid TYPE UUID USING uuid::UUID,
ALTER COLUMN still_available TYPE boolean USING still_available ='Still_avaliable',
ALTER COLUMN weight_class TYPE VARCHAR(14);


-- task 6


SELECT LENGTH(CAST(month AS TEXT))
FROM dim_date_times
GROUP BY month
ORDER BY LENGTH(CAST(month AS TEXT)) DESC
LIMIT 1; -- 2


SELECT LENGTH(CAST(day AS TEXT))
FROM dim_date_times
GROUP BY day
ORDER BY LENGTH(CAST(day AS TEXT)) DESC
LIMIT 1; -- 2

SELECT LENGTH(CAST(year AS TEXT))
FROM dim_date_times
GROUP BY year
ORDER BY LENGTH(CAST(year AS TEXT)) DESC
LIMIT 1; -- 4

SELECT LENGTH(CAST(time_period AS TEXT))
FROM dim_date_times
GROUP BY time_period
ORDER BY LENGTH(CAST(time_period AS TEXT)) DESC
LIMIT 1; -- 10


ALTER TABLE dim_date_times
ALTER COLUMN month TYPE VARCHAR(2),
ALTER COLUMN day TYPE VARCHAR(2),
ALTER COLUMN year TYPE VARCHAR(4),
ALTER COLUMN time_period TYPE VARCHAR(10),
ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID;

-- task 7

SELECT LENGTH(CAST(card_number AS TEXT))
FROM dim_card_details
GROUP BY card_number
ORDER BY LENGTH(CAST(card_number AS TEXT)) DESC
LIMIT 1; -- 22


SELECT LENGTH(CAST(expiry_date AS TEXT))
FROM dim_card_details
GROUP BY expiry_date
ORDER BY LENGTH(CAST(expiry_date AS TEXT)) DESC
LIMIT 1; -- 10

ALTER TABLE dim_card_details
ALTER COLUMN card_number TYPE VARCHAR(22),
ALTER COLUMN expiry_date TYPE VARCHAR(10),
ALTER COLUMN date_payment_confirmed TYPE DATE USING date_payment_confirmed::DATE


-- task 8

ALTER TABLE orders_table
DROP level_0;

ALTER TABLE dim_users
DROP level_0;

ALTER TABLE dim_products
DROP level_0;

ALTER TABLE dim_card_details
ADD CONSTRAINT pk_card_number PRIMARY KEY(card_number);

ALTER TABLE dim_date_times
ADD CONSTRAINT pk_date_uuid PRIMARY KEY(date_uuid);

ALTER TABLE dim_products
ADD CONSTRAINT pk_product_code PRIMARY KEY(product_code);

ALTER TABLE dim_store_details
ADD CONSTRAINT pk_store_code PRIMARY KEY(store_code);

ALTER TABLE dim_users
ADD CONSTRAINT pk_user_uuid PRIMARY KEY(user_uuid);


-- task 9

INSERT INTO dim_card_details (card_number)
SELECT DISTINCT ot.card_number
FROM orders_table ot
LEFT JOIN dim_card_details dcd ON ot.card_number = dcd.card_number
WHERE dcd.card_number IS NULL;

INSERT INTO dim_users (user_uuid)
SELECT DISTINCT du.user_uuid
FROM orders_table ot
LEFT JOIN dim_users du ON ot.card_number = du.user_uuid
WHERE du.user_uuid IS NULL;

INSERT INTO dim_store_details (store_code)
SELECT DISTINCT ot.store_code
FROM orders_table ot
LEFT JOIN dim_store_details dsd ON ot.store_code = dsd.store_code
WHERE dsd.store_code IS NULL;


INSERT INTO dim_products (product_code)
SELECT DISTINCT ot.product_code
FROM orders_table ot
LEFT JOIN dim_products dp ON ot.product_code = dp.product_code
WHERE dp.product_code IS NULL;




ALTER TABLE orders_table
ADD CONSTRAINT fk_date_uuid
FOREIGN KEY(date_uuid)
REFERENCES dim_date_times(date_uuid)


ALTER TABLE orders_table
ADD CONSTRAINT fk_user_uuid
FOREIGN KEY(user_uuid)
REFERENCES dim_users(user_uuid)


ALTER TABLE orders_table
ADD CONSTRAINT fk_card_number
FOREIGN KEY(card_number)
REFERENCES dim_card_details(card_number)


ALTER TABLE orders_table
ADD CONSTRAINT fk_store_code
FOREIGN KEY(store_code)
REFERENCES dim_store_details(store_code)


ALTER TABLE orders_table
ADD CONSTRAINT fk_product_code
FOREIGN KEY(product_code)
REFERENCES dim_products(product_code)


