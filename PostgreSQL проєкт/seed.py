import psycopg2
from faker import Faker
import random
from db_config import get_task_management_connection, get_db_cursor

fake = Faker(['uk_UA'])

# Ініціалізація змінних
conn = None
cur = None

try:
    # 🔌 Підключення через конфіг
    conn = get_task_management_connection()  
    cur = get_db_cursor(conn)
    
    print("🧹 Очищуємо таблиці...")
    
    # Крок 2: Очищення таблиць у ПРАВИЛЬНОМУ порядку
    cur.execute("DELETE FROM tasks;")    # Спочатку дочірні (з зовнішніми ключами)
    cur.execute("DELETE FROM users;")    # Потім батьківські  
    cur.execute("DELETE FROM status;")   # Потім батьківські
    print("✅ Таблиці очищені.")
    
    print("\n📊 Додаємо довідкові дані...")
    
    # Крок 3: Додаємо статуси
    statuses = [('new',), ('in progress',), ('completed',)]
    for status in statuses:
        cur.execute("INSERT INTO status (name) VALUES (%s);", status)
    print("✅ Статуси додані: new, in progress, completed")
    
    print("\n👥 Створюємо користувачів...")
    
    # Крок 4: Додаємо користувачів  
    for i in range(10):
        fullname = fake.name()
        email = fake.email()
        cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s);", (fullname, email))
    print("✅ Додано 10 користувачів з українськими іменами")
    
    print("\n📋 Створюємо завдання...")
    
    # Крок 5: Отримуємо ID для завдань
    cur.execute("SELECT id FROM users;")
    user_ids = [row[0] for row in cur.fetchall()]
    
    cur.execute("SELECT id FROM status;")
    status_ids = [row[0] for row in cur.fetchall()]
    
    print(f"📊 Знайдено користувачів: {len(user_ids)}, статусів: {len(status_ids)}")
    
    # Створюємо завдання
    for i in range(20):
        title = fake.sentence(nb_words=4)
        description = fake.text() if random.choice([True, False]) else None  # Іноді без опису
        user_id = random.choice(user_ids)
        status_id = random.choice(status_ids)
        
        cur.execute("""
            INSERT INTO tasks (title, description, user_id, status_id) 
            VALUES (%s, %s, %s, %s);
        """, (title, description, user_id, status_id))
    
    print("✅ Додано 20 завдань")
    
    # Комміт змін
    conn.commit()
    
    print("\n🎉 Всі дані успішно додані!")
    print("=" * 50)
    print("📊 СТАТИСТИКА:")
    
    cur.execute("SELECT COUNT(*) FROM users;")
    result = cur.fetchone()
    users_count = result[0] if result else 0

    cur.execute("SELECT COUNT(*) FROM status;")
    result = cur.fetchone()
    status_count = result[0] if result else 0

    cur.execute("SELECT COUNT(*) FROM tasks;")
    result = cur.fetchone()
    tasks_count = result[0] if result else 0
    
    print(f"👥 Користувачів: {users_count}")
    print(f"📊 Статусів: {status_count}")
    print(f"📋 Завдань: {tasks_count}")
    
    # Показуємо розподіл завдань за статусами
    cur.execute("""
        SELECT s.name, COUNT(t.id) 
        FROM status s 
        LEFT JOIN tasks t ON s.id = t.status_id 
        GROUP BY s.name
    """)
    
    print("\n📈 Розподіл завдань за статусами:")
    for status_name, count in cur.fetchall():
        print(f"  {status_name}: {count} завдань")
    
except psycopg2.Error as e:
    print(f"❌ Помилка: {e}")
    
finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
        print("\n🚪 З'єднання закрито.")