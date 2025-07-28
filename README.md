# 🗄️ Проєкт роботи з базами даних

Навчальний проєкт для вивчення роботи з **PostgreSQL** та **MongoDB** на Python.

## 📁 Структура проєкту

### PostgreSQL частина (Task Management)
```
📦 PostgreSQL проєкт
├── 🔧 db_config.py          # Конфігурація підключення до БД
├── 🏗️ create_tables.py      # Створення бази даних та таблиць
├── 🌱 seed.py               # Заповнення тестовими даними
├── 📖 queries_select.py     # SELECT запити (читання даних)
└── 📝 queries_crud.py       # CRUD операції (зміна даних)
```

### MongoDB частина (Cats Database)
```
📦 MongoDB проєкт
└── 🐱 main.py               # CRUD операції з котами в MongoDB
```

## 🚀 Встановлення та налаштування

### Крок 1: Встановлення залежностей
```bash
pip install psycopg2-binary faker pymongo
```

### Крок 2: Налаштування PostgreSQL
1. Встановіть PostgreSQL
2. Відредагуйте `db_config.py` під свої налаштування:
```python
# Замініть на свої дані
host="localhost"  
port="5432"
user="postgres"
password="ваш_пароль"
```

### Крок 3: Налаштування MongoDB
1. Встановіть MongoDB
2. Запустіть MongoDB сервіс
```bash
# Linux/Mac
sudo systemctl start mongod

# Windows  
net start MongoDB
```

## 🏗️ Запуск PostgreSQL проєкту

### 1. Створення бази та таблиць
```bash
python create_tables.py
```
**Результат:** Створює базу `task_management` з таблицями `users`, `tasks`, `status`

### 2. Заповнення тестовими даними
```bash
python seed.py
```
**Результат:** Додає 10 користувачів, 3 статуси, 20 завдань

### 📖 Читання даних
```bash
python queries_select.py
```
**Функції:**
- `query_1_user_tasks(user_id)` - завдання користувача
- `query_2_user_status(status)` - завдання за статусом  
- `query_3_search_user_email(email)` - пошук за email
- `query_4_users_not_task()` - користувачі без завдань
- `query_5_add_new_task_select()` - додати завдання (SELECT версія)
- `query_6_incomplete_tasks()` - незавершені завдання
- `query_10_count_by_status()` - кількість завдань за статусом
- `query_11_tasks_by_domain(domain)` - завдання за доменом email
- `query_12_tasks_no_description()` - завдання без опису
- `query_13_users_in_progress()` - користувачі з завданнями 'in progress'  
- `query_14_users_task_count()` - користувачі та кількість завдань

### 📝 CRUD операції
```bash
python queries_crud.py
```
**Функції:**
- `query_3_update_task_status(task_id, new_status)` - оновити статус
- `query_5_add_new_task(title, description, user_id)` - додати завдання  
- `query_7_delete_task(task_id)` - видалити завдання
- `query_9_update_user_name(user_id, new_name)` - оновити ім'я
- `show_database_stats()` - статистика БД

## 🐱 Запуск MongoDB проєкту

```bash
python main.py
```

**Інтерактивне меню:**
```
🐱 МЕНЮ:
1 - Показати всіх котів
2 - Знайти кота за ім'ям
3 - Оновити вік кота
4 - Додати особливість коту
5 - Видалити кота
6 - Видалити всіх котів
0 - Вихід
```

## 💾 Структура даних

### PostgreSQL таблиці

#### users
| Поле | Тип | Опис |
|------|-----|------|
| id | SERIAL | Унікальний ідентифікатор |
| fullname | VARCHAR(100) | Повне ім'я |
| email | VARCHAR(100) | Email (унікальний) |

#### status
| Поле | Тип | Опис |
|------|-----|------|
| id | SERIAL | Унікальний ідентифікатор |
| name | VARCHAR(50) | Назва статусу |

#### tasks
| Поле | Тип | Опис |
|------|-----|------|
| id | SERIAL | Унікальний ідентифікатор |
| title | VARCHAR(100) | Заголовок завдання |
| description | TEXT | Опис завдання |
| user_id | INTEGER | FK на users.id |
| status_id | INTEGER | FK на status.id |

### MongoDB колекція

#### cats
```json
{
  "_id": ObjectId,
  "name": "string",
  "age": number,
  "features": ["string", "string", ...]
}
```

## 📚 Приклади використання

### PostgreSQL приклади

#### Додати нове завдання
```python
# Через CRUD операції
from queries_crud import query_5_add_new_task
query_5_add_new_task("Вивчити Python", "Опанувати основи мови програмування", 1)

# Через SELECT запити  
from queries_select import query_5_add_new_task_select
query_5_add_new_task_select("Новий проєкт", "Створити веб-додаток", 2)
```

#### Знайти завдання за статусом
```python
from queries_select import query_2_user_status

query_2_user_status("new")  # Показує всі нові завдання
```

#### Оновити статус завдання
```python
from queries_crud import query_3_update_task_status

query_3_update_task_status(1, "completed")
```

### MongoDB приклади

#### Програмне додавання кота
```python
test_cat = {
    "name": "Мурзик",
    "age": 2,
    "features": ["грайливий", "любить рибу", "сірий"]
}
collection.insert_one(test_cat)
```

#### Пошук кота
```python
cat = collection.find_one({"name": "Мурзик"})
```

## 📖 Корисні команди

### PostgreSQL
```sql
-- Подивитися всі бази
\l

-- Підключитися до бази
\c task_management

-- Подивитися таблиці
\dt

-- Подивитися структуру таблиці
\d users
```

### MongoDB
```javascript
// Подивитися всі бази
show dbs

// Використати базу
use cats_database

// Подивитися колекції
show collections

// Знайти всі документи
db.cats.find().pretty()
```
