import psycopg2
from db_config import get_postgres_connection, get_task_management_connection, get_db_cursor

# Ініціалізація змінних
conn = None
cur = None

try:
    # 🗂️ ЕТАП 1: Створення бази даних
    print("🗂️ Створюємо базу даних...")
    
    conn = get_postgres_connection()  # 🎉 ПРОСТО!
    conn.autocommit = True
    cur = get_db_cursor(conn)
    
    cur.execute("CREATE DATABASE task_management;")
    print("✅ База даних task_management створена.")
    
except psycopg2.Error as e:
    if "already exists" in str(e):
        print("ℹ️ База даних task_management вже існує.")
    else:
        print(f"❌ Помилка при створенні БД: {e}")
finally:
    if cur:
        cur.close()
    if conn:
        conn.close()

try:
    # 🏗️ ЕТАП 2: Створення таблиць
    print("\n🏗️ Створюємо таблиці...")
    
    conn = get_task_management_connection()  # 🎉 ПРОСТО!
    cur = get_db_cursor(conn)

    # 👥 Таблиця користувачів
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            fullname VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        );
    """)
    print("✅ Таблиця users створена.")
    
    # 📊 Таблиця статусів
    cur.execute("""
        CREATE TABLE IF NOT EXISTS status (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        );
    """)
    print("✅ Таблиця status створена.")
    
    # 📝 Таблиця завдань
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            status_id INTEGER REFERENCES status(id),
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    print("✅ Таблиця tasks створена.")
    
    # Фіксація змін
    conn.commit()
    print("\n🎉 Всі таблиці створені в базі task_management!")
    
except psycopg2.Error as e:
    print(f"❌ Помилка при створенні таблиць: {e}")
    
finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
        print("🚪 З'єднання з базою даних закрито.")