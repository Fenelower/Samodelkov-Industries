import psycopg2
import pandas as pd

# ---------- Настройки подключения ----------
DB_HOST = 'localhost'
DB_NAME = 'MAXIMVISUAL'
DB_USER = 'postgres'
DB_PASS = 'maxim22s2'
DB_PORT = 5433 

# ---------- Подключение к БД ----------
conn = psycopg2.connect(
    host=DB_HOST,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    port=DB_PORT
)

# ---------- SQL-запросы ----------
queries = {
    "Клиенты по штатам": """
        SELECT customer_state, COUNT(*) AS num_customers
        FROM customers
        GROUP BY customer_state
        ORDER BY num_customers DESC;
    """,
    "Топ городов по уникальным клиентам": """
        SELECT customer_city, COUNT(DISTINCT customer_unique_id) AS unique_customers
        FROM customers
        GROUP BY customer_city
        ORDER BY unique_customers DESC
        LIMIT 10;
    """,
    "Клиенты из штата SP": """
        SELECT customer_id, customer_city, customer_state
        FROM customers
        WHERE customer_state = 'SP'
        ORDER BY customer_city;
    """
}

# ---------- Выполнение запросов ----------
for name, query in queries.items():
    print(f"\n--- {name} ---")
    df = pd.read_sql(query, conn)
    print(df)
    # Сохраняем результаты в CSV
    df.to_csv(f"{name.replace(' ', '_')}.csv", index=False)

# ---------- Закрываем соединение ----------
conn.close()
print("\nВсе запросы выполнены и сохранены в CSV.")
