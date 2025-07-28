# queries_crud.py - INSERT/UPDATE/DELETE запити для зміни даних

from db_config import get_task_management_connection, get_db_cursor

def query_3_update_task_status(task_id, new_status):
    """🔄 3. Оновити статус завдання"""
    
    conn = None
    cur = None
    
    try:
        conn = get_task_management_connection()
        cur = get_db_cursor(conn)
        
        # Перевіряємо чи існує завдання
        cur.execute("SELECT title, status_id FROM tasks WHERE id = %s", (task_id,))
        task = cur.fetchone()
        
        if not task:
            print(f"❌ Завдання з ID {task_id} не знайдено")
            return
        
        # Перевіряємо чи існує такий статус
        cur.execute("SELECT id FROM status WHERE name = %s", (new_status,))
        status = cur.fetchone()
        
        if not status:
            print(f"❌ Статус '{new_status}' не існує")
            print("💡 Доступні статуси: new, in progress, completed")
            return
        
        # Показуємо що оновлюємо
        cur.execute("""
            SELECT s.name FROM status s WHERE s.id = %s
        """, (task[1],))
        current_status = cur.fetchone()
        
        print(f"📋 Завдання: {task[0]}")
        print(f"📊 Поточний статус: {current_status[0] if current_status else 'невідомо'}")
        print(f"🔄 Новий статус: {new_status}")
        
        # Запит на оновлення
        cur.execute("""
            UPDATE tasks 
            SET status_id = %s
            WHERE id = %s
        """, (status[0], task_id))
        
        conn.commit()
        print(f"✅ Статус завдання {task_id} успішно оновлено!")
            
    except Exception as e:
        print(f"❌ Помилка при оновленні статусу: {e}")
        
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def query_5_add_new_task(title, description, user_id):
    """➕ 5. Додати нове завдання"""  
    
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

        # Запит на додавання
        cur.execute("""
            INSERT INTO tasks (title, description, user_id, status_id) 
            VALUES (%s, %s, %s, (SELECT id FROM status WHERE name = 'new'))
        """, (title, description, user_id))

        conn.commit()
        
        # Отримуємо ID нового завдання
        new_task_id = cur.lastrowid
        print(f"✅ Завдання '{title}' успішно додано!")
        print(f"🆔 ID нового завдання: {new_task_id if new_task_id else 'невідомо'}")
        print(f"📊 Статус: new")

    except Exception as e:
        print(f"❌ Помилка при додаванні завдання: {e}")    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        

def query_7_delete_task(task_id):
    """🗑️ 7. Видалити завдання"""
    conn = None
    cur = None
    
    try:
        conn = get_task_management_connection()
        cur = get_db_cursor(conn)
    
        # Перевіряємо чи існує завдання
        cur.execute("""
            SELECT t.title, u.fullname, s.name 
            FROM tasks t
            LEFT JOIN users u ON t.user_id = u.id
            LEFT JOIN status s ON t.status_id = s.id
            WHERE t.id = %s
        """, (task_id,))
        task = cur.fetchone()
        
        if not task:
            print(f"❌ Завдання з ID {task_id} не знайдено")
            # Показуємо доступні завдання
            cur.execute("SELECT id, title FROM tasks LIMIT 5")
            tasks = cur.fetchall()
            print("💡 Доступні завдання:")
            for t in tasks:
                print(f"   ID: {t[0]} - {t[1]}")
            return
        
        # Показуємо що видаляємо
        print(f"🗑️ Видалення завдання:")
        print(f"   📝 Назва: {task[0]}")
        print(f"   👤 Користувач: {task[1] or 'невідомо'}")
        print(f"   📊 Статус: {task[2] or 'невідомо'}")
        
        # Запит на видалення
        cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        
        conn.commit()
        print(f"✅ Завдання {task_id} успішно видалено!")
        
    except Exception as e:
        print(f"❌ Помилка при видаленні завдання: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def query_9_update_user_name(user_id, new_name):
    """✏️ 9. Оновити ім'я користувача"""
    conn = None
    cur = None
    
    try:
        conn = get_task_management_connection()
        cur = get_db_cursor(conn)
        
        # Перевіряємо чи існує користувач
        cur.execute("SELECT fullname, email FROM users WHERE id = %s", (user_id,))
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
        
        # Показуємо що оновлюємо
        print(f"✏️ Оновлення користувача:")
        print(f"   👤 Поточне ім'я: {user[0]}")
        print(f"   📧 Email: {user[1]}")
        print(f"   🔄 Нове ім'я: {new_name}")
        
        # Запит на оновлення
        cur.execute("UPDATE users SET fullname = %s WHERE id = %s", (new_name, user_id))
        
        conn.commit()
        print(f"✅ Ім'я користувача {user_id} успішно оновлено!")
            
    except Exception as e:
        print(f"❌ Помилка при оновленні імені: {e}")
        
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def show_database_stats():
    """📊 Показати статистику бази даних"""
    conn = None
    cur = None
    
    try:
        conn = get_task_management_connection()
        cur = get_db_cursor(conn)
        
        print("\n📊 СТАТИСТИКА БАЗИ ДАНИХ:")
        print("=" * 50)
        
        # Кількість користувачів
        cur.execute("SELECT COUNT(*) FROM users")
        result = cur.fetchone()
        users_count = result[0] if result else 0
        print(f"👥 Користувачів: {users_count}")
        
        # Кількість завдань
        cur.execute("SELECT COUNT(*) FROM tasks")
        result = cur.fetchone()
        tasks_count = result[0] if result else 0    
        print(f"📝 Завдань: {tasks_count}")
        
        # Статистика по статусах
        cur.execute("""
            SELECT s.name, COUNT(t.id) 
            FROM status s 
            LEFT JOIN tasks t ON s.id = t.status_id 
            GROUP BY s.name
        """)
        status_stats = cur.fetchall()
        print(f"\n📈 Розподіл завдань по статусах:")
        for status, count in status_stats:
            print(f"   {status}: {count} завдань")
            
    except Exception as e:
        print(f"❌ Помилка при отриманні статистики: {e}")
        
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # Тести CRUD операцій
    #query_3_update_task_status(23, '3')
    #query_5_add_new_task('Тестове завдання', 'Опис завдання', 2)
    #query_7_delete_task(22)
    query_9_update_user_name(18,'Нове3 Імя')