-- Initialize Olist datasets in PostgreSQL
CREATE TABLE IF NOT EXISTS olist_customers (
    customer_id TEXT PRIMARY KEY,
    customer_unique_id TEXT,
    customer_zip_code_prefix INTEGER,
    customer_city TEXT,
    customer_state TEXT
);

CREATE TABLE IF NOT EXISTS olist_orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT REFERENCES olist_customers(customer_id),
    order_status TEXT,
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP NULL,
    order_delivered_carrier_date TIMESTAMP NULL,
    order_delivered_customer_date TIMESTAMP NULL,
    order_estimated_delivery_date TIMESTAMP
);

\copy olist_customers (customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state)
FROM '/docker-entrypoint-initdb.d/datasets/olist_customers_dataset23.csv'
DELIMITER ',' CSV HEADER;

\copy olist_orders (order_id, customer_id, order_status, order_purchase_timestamp, order_approved_at,
                     order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date)
FROM '/docker-entrypoint-initdb.d/datasets/olist_orders_dataset.csv'
DELIMITER ',' CSV HEADER;
