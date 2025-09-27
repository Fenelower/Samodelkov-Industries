import psycopg2
import pandas as pd

conn = psycopg2.connect(
    dbname="MAXIMVISUAL",
    user="postgres",
    password="maxim22s2",
    host="localhost",
    port="5433"
)

queries = {
    # 1 Среднее время доставки (в днях)
    "AVG_DELIVERY_DAYS": """
        SELECT ROUND(AVG(EXTRACT(DAY FROM order_delivered_customer_date - order_purchase_timestamp)), 2) 
        AS avg_delivery_days
        FROM orders
        WHERE order_delivered_customer_date IS NOT NULL;
    """,

    # 2 Кол-во заказов по штатам
    "ORDERS_BY_STATE": """
        SELECT customer_state, COUNT(*) AS orders_count
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY customer_state
        ORDER BY orders_count DESC
        LIMIT 10;
    """,

    # 3 Средний рейтинг отзывов
    "AVG_REVIEW_SCORE": """
        SELECT ROUND(AVG(review_score), 2) AS avg_review_score
        FROM reviews;
    """,

    # 4 10 самых дорогих заказов
    "TOP_ORDERS_BY_PRICE": """
        SELECT order_id, SUM(price) AS total_price
        FROM order_items
        GROUP BY order_id
        ORDER BY total_price DESC
        LIMIT 10;
    """,

    # 5 Самые популярные категории товаров
    "TOP_PRODUCT_CATEGORIES": """
        SELECT p.product_category_name, COUNT(*) AS total_sold
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY p.product_category_name
        ORDER BY total_sold DESC
        LIMIT 10;
    """,

    # 6 Средняя стоимость доставки (freight_value)
    "AVG_FREIGHT_VALUE": """
        SELECT ROUND(AVG(freight_value), 2) AS avg_freight
        FROM order_items;
    """,

    # 7 Средний чек по заказу (сумма price)
    "AVG_ORDER_VALUE": """
        SELECT ROUND(AVG(total), 2) AS avg_order_value
        FROM (
            SELECT order_id, SUM(price) AS total
            FROM order_items
            GROUP BY order_id
        ) t;
    """,

    # 8 Количество заказов по месяцам
    "ORDERS_BY_MONTH": """
        SELECT DATE_TRUNC('month', order_purchase_timestamp) AS month, COUNT(*) AS orders_count
        FROM orders
        GROUP BY month
        ORDER BY month;
    """,

    # 9 Среднее количество товаров в заказе
    "AVG_ITEMS_PER_ORDER": """
        SELECT ROUND(AVG(items), 2) AS avg_items_per_order
        FROM (
            SELECT order_id, COUNT(*) AS items
            FROM order_items
            GROUP BY order_id
        ) t;
    """,

    # 10 Количество отзывов по оценкам
    "REVIEWS_DISTRIBUTION": """
        SELECT review_score, COUNT(*) AS reviews_count
        FROM reviews
        GROUP BY review_score
        ORDER BY review_score;
    """
}

results = {}

for name, query in queries.items():
    df = pd.read_sql(query, conn)
    results[name] = df
    print(f"\n{name}:")
    print(df)

print("\nВсе запросы выполнены")
conn.close()
