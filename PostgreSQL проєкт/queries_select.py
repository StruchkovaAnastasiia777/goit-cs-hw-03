from db_config import get_task_management_connection, get_db_cursor

def query_1_user_tasks(user_id):
    """📋 1. Отримати всі завдання користувача за user_id"""
    
    conn = None
    cur = None
    
    try:
        # 🔌 Підключення
        conn = get_task_management_connection()
        cur = get_db_cursor(conn)
        
        # ⚡ Твій SQL запит
        cur.execute("""
            SELECT user_id, title, description
            FROM tasks t
            WHERE user_id = %s
        """, (user_id,))
        
        # 📊 Отримання результату
        results = cur.fetchall()
        
        # 🎨 Гарний вивід
        if results:
            print(f"\n📋 Завдання користувача {user_id}:")
            print(f"Всього завдань: {len(results)}")
            print("Заголовок та опис:")
            print("-" * 50)
            for task in results:
                print(f"✅ {task[1]}")
                if task[2]:
                    print(f"   💬 {task[2]}")
                else:
                    print(f"   💬 Без опису")
        else:
            print(f"❌ У користувача {user_id} немає завдань")
            
    except Exception as e:
        print(f"❌ Помилка: {e}")
        
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

            
def query_2_user_status(name):
    """📊 2. Завдання за статусом"""
    
    conn = None
    cur = None

    try:
        conn = get_task_management_connection()
        cur = get_db_cursor(conn)
        
        cur.execute("""
            SELECT t.status_id, s.name, t.title, t.description
            FROM tasks t
            LEFT JOIN status s ON t.status_id = s.id
            WHERE s.name = %s
        """, (name,))
     
        results = cur.fetchall()
        
        if results:
            print(f"\n📊 Завдання зі статусом '{name}':")
            print(f"Всього завдань: {len(results)}")
            print("-" * 50)
            for task in results:
                print(f"✅ **Заголовок**: {task[2]}")
                print(f"📊 Статус: {task[1]} (ID: {task[0]})")
                if task[3]:  # ✅ Перевіряємо description
                    print(f"💬 Опис: {task[3]}")
                else:
                    print("💬 Без опису")
                print("_" * 50)
        else:
            print(f"❌ Немає завдань зі статусом '{name}'") 
                
    except Exception as e:
        print(f"❌ Помилка: {e}")
        
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def query_3_search_user_email(email):
    """🔍 3. Пошук користувача за ім'ям і email"""
    
    conn = None
    cur = None
    
    try:
        conn = get_task_management_connection()
        cur = get_db_cursor(conn)
        
        cur.execute("""
            SELECT fullname, email
            FROM users 
            WHERE email ILIKE %s
        """, (f'%{email}%',)) 
        
        results = cur.fetchall()
        
        if results:
            print(f"\n🔍 Знайдені користувачі з '{email}' у email:")
            print("-" * 50)
            for user in results:
                print(f"👤 Ім'я: {user[0]}, Email: {user[1]}") 
            print(f"\nВсього знайдено: {len(results)}")
        else:
            print(f"❌ Користувачі з '{email}' у email не знайдені")
            
    except Exception as e:
        print(f"❌ Помилка: {e}")
        
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def query_4_users_not_task():
    """👥 4. Користувачі без завдань"""

    conn = None
    cur = None
    
    try:
        conn = get_task_management_connection()
        cur = get_db_cursor(conn)
        
        # ✅ Користувачі БЕЗ завдань
        cur.execute("""
            SELECT u.id, u.fullname, u.email
            FROM users u
            LEFT JOIN tasks t ON u.id = t.user_id
            WHERE t.user_id IS NULL
        """)
        
        results = cur.fetchall()
        
        if results:
            print("\n👥 Користувачі без завдань:")
            print(f"Всього знайдено: {len(results)}")
            print("-" * 50)
            for user in results:
                print(f"👤 ID: {user[0]} | {user[1]} ({user[2]})")
        else:
            print("✅ Всі користувачі мають завдання")
            
    except Exception as e:
        print(f"❌ Помилка: {e}")
        
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def query_5_add_new_task_select(title, description, user_id):
    """➕ 5. Додати нове завдання для конкретного користувача"""
    
    conn = None
    cur = None
    
    try:
        conn = get_task_management_connection()
        cur = get_db_cursor(conn)

        # Перевіряємо чи існує користувач
        cur.execute("SELECT fullname FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        
        if not user:
            print(f"❌ Користувач з ID {user_id} не знайдений")
            # Показуємо доступних користувачів
            cur.execute("SELECT id, fullname FROM users LIMIT 5")
            users = cur.fetchall()
            print("💡 Доступні користувачі:")
            for u in users:
                print(f"   ID: {u[0]} - {u[1]}")
            return
        
        # Показуємо що додаємо
        print(f"👤 Користувач: {user[0]}")
        print(f"📝 Завдання: {title}")
        print(f"💬 Опис: {description[:50]}..." if len(description) > 50 else f"💬 Опис: {description}")

        # Запит на додавання з поверненням ID
        cur.execute("""
            INSERT INTO tasks (title, description, user_id, status_id) 
            VALUES (%s, %s, %s, (SELECT id FROM status WHERE name = 'new'))
            RETURNING id
        """, (title, description, user_id))
        result = cur.fetchone()
        if result:
            new_task_id = result[0]
            conn.commit()
    
            print(f"✅ Завдання '{title}' успішно додано!")
            print(f"🆔 ID нового завдання: {new_task_id}")
            print(f"📊 Статус: new")
        else:
            print("❌ Не вдалося додати завдання")

    except Exception as e:
        print(f"❌ Помилка при додаванні завдання: {e}")    
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def query_6_incomplete_tasks():
    """📋 6. Отримати всі завдання, які ще не завершено"""
    
    conn = None
    cur = None
    
    try:
        conn = get_task_management_connection()
        cur = get_db_cursor(conn)
        
        cur.execute("""
            SELECT t.id, t.title, u.fullname, s.name
            FROM tasks t
            JOIN users u ON t.user_id = u.id
            JOIN status s ON t.status_id = s.id
            WHERE s.name != 'completed'
        """)
        
        results = cur.fetchall()
        
        if results:
            print(f"\n📋 Незавершені завдання:")
            print(f"Всього знайдено: {len(results)}")
            print("-" * 50)
            for task in results:
                print(f"🆔 ID: {task[0]} | 📝 {task[1]}")
                print(f"👤 Користувач: {task[2]}")
                print(f"📊 Статус: {task[3]}")
                print("_" * 50)
        else:
            print("✅ Всі завдання завершені!")
            
    except Exception as e:
        print(f"❌ Помилка: {e}")
        
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def query_10_count_by_status():
    """📊 10. Кількість завдань для кожного статусу"""
    
    conn = None
    cur = None
    
    try:
        conn = get_task_management_connection()
        cur = get_db_cursor(conn)
        
        cur.execute("""
            SELECT s.name, COUNT(t.id) as task_count
            FROM status s
            LEFT JOIN tasks t ON s.id = t.status_id
            GROUP BY s.name
        """)
        
        results = cur.fetchall()
        
        if results:
            print(f"\n📊 Кількість завдань по статусах:")
            print("-" * 50)
            total_tasks = 0
            for status_name, count in results:
                print(f"📈 {status_name}: {count} завдань")
                total_tasks += count
            print(f"\n🔢 Загалом завдань: {total_tasks}")
        else:
            print("❌ Статуси не знайдені")
            
    except Exception as e:
        print(f"❌ Помилка: {e}")
        
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def query_11_tasks_by_domain(domain):
    """🌐 11. Завдання користувачів з певним доменом email"""
    
    conn = None
    cur = None
    
    try:
        conn = get_task_management_connection()
        cur = get_db_cursor(conn)
        
        cur.execute("""
            SELECT t.title, u.fullname, u.email
            FROM tasks t
            JOIN users u ON t.user_id = u.id
            WHERE u.email LIKE %s
        """, (f'%{domain}%',))
        
        results = cur.fetchall()
        
        if results:
            print(f"\n🌐 Завдання користувачів з доменом '{domain}':")
            print(f"Всього знайдено: {len(results)}")
            print("-" * 50)
            for task in results:
                print(f"📝 Завдання: {task[0]}")
                print(f"👤 Користувач: {task[1]} ({task[2]})")
                print("_" * 50)
        else:
            print(f"❌ Завдань з доменом '{domain}' не знайдено")
            
    except Exception as e:
        print(f"❌ Помилка: {e}")
        
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def query_12_tasks_no_description():
    """📝 12. Завдання без опису"""
    
    conn = None
    cur = None
    
    try:
        conn = get_task_management_connection()
        cur = get_db_cursor(conn)
        
        cur.execute("""
            SELECT t.id, t.title, u.fullname
            FROM tasks t
            JOIN users u ON t.user_id = u.id
            WHERE t.description IS NULL OR t.description = ''
        """)
        
        results = cur.fetchall()
        
        if results:
            print(f"\n📝 Завдання без опису:")
            print(f"Всього знайдено: {len(results)}")
            print("-" * 50)
            for task in results:
                print(f"🆔 ID: {task[0]} | 📝 {task[1]}")
                print(f"👤 Користувач: {task[2]}")
                print("_" * 50)
        else:
            print("✅ Всі завдання мають опис!")
            
    except Exception as e:
        print(f"❌ Помилка: {e}")
        
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def query_13_users_in_progress():
    """🔄 13. Користувачі та їх завдання в статусі 'in progress'"""
    
    conn = None
    cur = None
    
    try:
        conn = get_task_management_connection()
        cur = get_db_cursor(conn)
        
        cur.execute("""
            SELECT u.fullname, t.title
            FROM users u
            INNER JOIN tasks t ON u.id = t.user_id
            INNER JOIN status s ON t.status_id = s.id
            WHERE s.name = 'in progress'
        """)
        
        results = cur.fetchall()
        
        if results:
            print(f"\n🔄 Користувачі та завдання в статусі 'in progress':")
            print(f"Всього знайдено: {len(results)}")
            print("-" * 50)
            for user_task in results:
                print(f"👤 {user_task[0]}: 📝 {user_task[1]}")
        else:
            print("❌ Немає завдань в статусі 'in progress'")
            
    except Exception as e:
        print(f"❌ Помилка: {e}")
        
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def query_14_users_task_count():
    """👥 14. Користувачі та кількість їх завдань"""
    
    conn = None
    cur = None
    
    try:
        conn = get_task_management_connection()
        cur = get_db_cursor(conn)
        
        cur.execute("""
            SELECT u.fullname, COUNT(t.id) as task_count
            FROM users u
            LEFT JOIN tasks t ON u.id = t.user_id
            GROUP BY u.id, u.fullname
            ORDER BY task_count DESC
        """)
        
        results = cur.fetchall()
        
        if results:
            print(f"\n👥 Користувачі та кількість їх завдань:")
            print("-" * 50)
            for user_data in results:
                print(f"👤 {user_data[0]}: {user_data[1]} завдань")
        else:
            print("❌ Користувачі не знайдені")
            
    except Exception as e:
        print(f"❌ Помилка: {e}")
        
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":

    
    # Приклади викликів функцій
    # query_1_user_tasks(17)  # Заміни 1 на потрібний user_id
    # query_2_user_status('new')  # Заміни 'new' на потрібний статус
    # query_3_search_user_email('com') # Заміни 'com' на потрібний email
    # query_4_users_not_task()  # Вивід користувачів без завдань
    # query_5_add_new_task_select('Тестове завдання', 'Опис тестового завдання', 1)
    # query_6_incomplete_tasks()  # Незавершені завдання
    # query_10_count_by_status()  # Кількість завдань за статусом  
    # query_11_tasks_by_domain('gmail.com')  # Завдання за доменом
    # query_12_tasks_no_description()  # Завдання без опису
    # query_13_users_in_progress()  # Користувачі з завданнями 'in progress'
    #query_14_users_task_count()  # Користувачі та кількість завдань
    pass