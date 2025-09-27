-- =====================================================
-- customers_setup.sql
-- Скрипт для создания таблицы customers и импорта CSV
-- =====================================================

-- Удаляем таблицу, если она уже существует
DROP TABLE IF EXISTS customers;

-- Создаём таблицу
CREATE TABLE customers (
    customer_id VARCHAR(50),
    customer_unique_id VARCHAR(50),
    customer_zip_code_prefix VARCHAR(20),
    customer_city VARCHAR(100),
    customer_state VARCHAR(10)
);

-- Импорт данных из CSV
\copy customers(customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state)
FROM 'C:/Users/Пользователь/Desktop/Новая папка (5)/2313/olist_customers_dataset2.csv'
DELIMITER ','
CSV HEADER;

-- Проверка первых 10 строк
SELECT * FROM customers
LIMIT 10;

