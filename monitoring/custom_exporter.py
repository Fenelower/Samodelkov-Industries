from prometheus_client import start_http_server, Gauge
import psycopg2
import time

# === Метрики Samodelkov Industries ===
customers_total = Gauge('si_customers_total', 'Total number of customers')
orders_total = Gauge('si_orders_total', 'Total number of orders')
products_total = Gauge('si_products_total', 'Total number of products')
average_payment_value = Gauge('si_avg_payment_value', 'Average payment value')
reviews_total = Gauge('si_reviews_total', 'Total number of reviews')
average_review_score = Gauge('si_avg_review_score', 'Average review score')

def collect_metrics():
    try:
        conn = psycopg2.connect(
            host="superset_db",      # контейнер PostgreSQL из Superset
            port=5432,               # внутренний порт контейнера
            database="MAXIMVISUAL",
            user="postgres",
            password="maxim22s2"
        )
        cur = conn.cursor()

        # === Метрики по таблицам ===
        cur.execute("SELECT COUNT(*) FROM customers;")
        customers_total.set(cur.fetchone()[0])

        cur.execute("SELECT COUNT(*) FROM orders;")
        orders_total.set(cur.fetchone()[0])

        cur.execute("SELECT COUNT(*) FROM products;")
        products_total.set(cur.fetchone()[0])

        cur.execute("SELECT AVG(payment_value) FROM payments;")
        avg_payment = cur.fetchone()[0]
        average_payment_value.set(avg_payment if avg_payment else 0)

        cur.execute("SELECT COUNT(*) FROM reviews;")
        reviews_total.set(cur.fetchone()[0])

        cur.execute("SELECT AVG(review_score) FROM reviews;")
        avg_review = cur.fetchone()[0]
        average_review_score.set(avg_review if avg_review else 0)

        cur.close()
        conn.close()
        print("✅ Metrics updated successfully")

    except Exception as e:
        print("❌ Error collecting metrics:", e)

if __name__ == "__main__":
    print("🚀 Starting Samodelkov Industries Custom Exporter...")
    start_http_server(8000)
    while True:
        print("🔄 Collecting metrics...")
        collect_metrics()
        time.sleep(20)

