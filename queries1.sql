-- =====================================================
-- queries.sql
-- SQL-запросы для аналитики таблицы customers
-- =====================================================

-- Количество клиентов по каждому штату
-- Считает количество клиентов в каждом штате
SELECT customer_state, COUNT(*) AS num_customers
FROM customers
GROUP BY customer_state
ORDER BY num_customers DESC;

-- Количество уникальных клиентов
-- Считает общее количество уникальных клиентов
SELECT COUNT(DISTINCT customer_unique_id) AS unique_customers
FROM customers;

-- Количество клиентов по городам
-- Считает количество клиентов в каждом городе
SELECT customer_city, COUNT(*) AS num_customers
FROM customers
GROUP BY customer_city
ORDER BY num_customers DESC
LIMIT 10;

-- Минимальный и максимальный почтовый индекс по штатам
-- Показывает минимальный и максимальный ZIP по каждому штату
SELECT customer_state, MIN(customer_zip_code_prefix) AS min_zip, MAX(customer_zip_code_prefix) AS max_zip
FROM customers
GROUP BY customer_state;

-- Список первых 10 клиентов
-- Показывает первые 10 клиентов
SELECT * 
FROM customers
LIMIT 10;

-- Фильтрация: клиенты из конкретного штата
-- Показывает клиентов из штата 'SP', отсортированных по городу
SELECT customer_id, customer_city, customer_state
FROM customers
WHERE customer_state = 'SP'
ORDER BY customer_city;

-- Количество клиентов в каждом ZIP-коде
-- Считает количество клиентов для каждого ZIP-кода
SELECT customer_zip_code_prefix, COUNT(*) AS num_customers
FROM customers
GROUP BY customer_zip_code_prefix
ORDER BY num_customers DESC
LIMIT 10;

-- Топ-10 городов с наибольшим количеством уникальных клиентов
-- Считает уникальных клиентов по городам
SELECT customer_city, COUNT(DISTINCT customer_unique_id) AS unique_customers
FROM customers
GROUP BY customer_city
ORDER BY unique_customers DESC
LIMIT 10;

-- Проверка повторяющихся customer_id
-- Находит customer_id, которые встречаются более одного раза
SELECT customer_id, COUNT(*) AS count_duplicates
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;

-- Статистика количества клиентов по первой букве города
-- Считает количество клиентов по первой букве названия города
SELECT LEFT(customer_city, 1) AS city_initial, COUNT(*) AS num_customers
FROM customers
GROUP BY city_initial
ORDER BY num_customers DESC;
