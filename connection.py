import psycopg2

try:
    conn = psycopg2.connect(
        dbname="contacts_db",
        user="postgres",
        password="ashish2002",
        host="localhost",
        port="5432"
    )
    print("✅ Database connected successfully!")
except Exception as e:
    print("❌ Database connection error:", e)
