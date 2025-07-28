from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

try:
    # Підключення до локальної MongoDB
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    # Перевіряємо підключення
    client.admin.command('ping')
    db = client.cats_database
    collection = db.cats
    print("✅ Підключення до MongoDB успішне!")
except (ConnectionFailure, ServerSelectionTimeoutError) as e:
    print(f"❌ Помилка підключення до MongoDB: {e}")
    print("💡 Переконайтеся що MongoDB запущений на localhost:27017")
    exit(1)
except Exception as e:
    print(f"❌ Несподівана помилка: {e}")
    exit(1)

# 1. 📖 READ - показати всіх котів
def read_all():
    """Показати всіх котів"""
    print("\n🐱 Всі коти в базі даних:")
    cats = collection.find()
    count = 0
    for cat in cats:
        count += 1
        print(f"{count}. {cat['name']}, вік: {cat['age']}, особливості: {cat['features']}")
    
    if count == 0:
        print("❌ Котів в базі даних немає")

# 2. 📖 READ - знайти кота за ім'ям
def read_by_name():
    """Знайти кота за ім'ям"""
    try:
        name = input("🔍 Введіть ім'я кота: ")
        cat = collection.find_one({"name": name})
        
        if cat:
            print(f"\n🐱 Знайдено кота:")
            print(f"   Ім'я: {cat['name']}")
            print(f"   Вік: {cat['age']}")
            print(f"   Особливості: {cat['features']}")
        else:
            print(f"❌ Кот з ім'ям '{name}' не знайдений")
    except Exception as e:
        print(f"❌ Помилка при пошуку кота: {e}")

# 3. 📝 UPDATE - оновити вік кота
def update_age():
    """Оновити вік кота"""
    try:
        name = input("🐱 Введіть ім'я кота: ")
        cat = collection.find_one({"name": name})
        
        if not cat:
            print(f"❌ Кот з ім'ям '{name}' не знайдений")
            return
        
        print(f"📋 Поточний вік {name}: {cat['age']} років")
        new_age = int(input("🔢 Введіть новий вік: "))
        
        if new_age < 0 or new_age > 30:
            print("❌ Неправильний вік! Введіть число від 0 до 30")
            return
        
        collection.update_one({"name": name}, {"$set": {"age": new_age}})
        print(f"✅ Вік кота {name} оновлено на {new_age} років")
    except ValueError:
        print("❌ Введіть правильне число для віку!")
    except Exception as e:
        print(f"❌ Помилка при оновленні віку: {e}")

# 4. 📝 UPDATE - додати характеристику
def add_feature():
    """Додати нову характеристику коту"""
    try:
        name = input("🐱 Введіть ім'я кота: ")
        cat = collection.find_one({"name": name})
        
        if not cat:
            print(f"❌ Кот з ім'ям '{name}' не знайдений")
            return
        
        print(f"📋 Поточні особливості {name}: {cat['features']}")
        new_feature = input("➕ Введіть нову особливість: ").strip()
        
        if not new_feature:
            print("❌ Особливість не може бути пустою!")
            return
        
        if new_feature in cat['features']:
            print(f"⚠️ Особливість '{new_feature}' вже існує!")
            return
        
        collection.update_one({"name": name}, {"$push": {"features": new_feature}})
        print(f"✅ Особливість '{new_feature}' додана коту {name}")
    except Exception as e:
        print(f"❌ Помилка при додаванні особливості: {e}")

# 5. 🗑️ DELETE - видалити кота за ім'ям
def delete_by_name():
    """Видалити кота за ім'ям"""
    try:
        name = input("🐱 Введіть ім'я кота для видалення: ")
        cat = collection.find_one({"name": name})
        
        if not cat:
            print(f"❌ Кот з ім'ям '{name}' не знайдений")
            return
        
        print(f"🗑️ Видаляємо кота: {cat['name']}, {cat['age']} років")
        confirm = input("❓ Точно видалити? (так/ні): ")
        
        if confirm.lower() in ['так', 'yes', 'y']:
            result = collection.delete_one({"name": name})
            if result.deleted_count > 0:
                print(f"✅ Кот {name} видалений")
            else:
                print(f"❌ Помилка при видаленні кота {name}")
        else:
            print("❌ Видалення скасовано")
    except Exception as e:
        print(f"❌ Помилка при видаленні кота: {e}")

# 6. 🗑️ DELETE - видалити всіх котів
def delete_all():
    """Видалити всіх котів"""
    try:
        count = collection.count_documents({})
        
        if count == 0:
            print("❌ В базі даних немає котів")
            return
        
        print(f"🗑️ В базі даних {count} котів")
        confirm = input("❓ Видалити ВСІХ котів? (так/ні): ")
        
        if confirm.lower() in ['так', 'yes', 'y']:
            result = collection.delete_many({})
            print(f"✅ Видалено {result.deleted_count} котів")
        else:
            print("❌ Видалення скасовано")
    except Exception as e:
        print(f"❌ Помилка при видаленні котів: {e}")

# Головне меню
def main_menu():
    """Головне меню"""
    while True:
        print("\n🐱 МЕНЮ:")
        print("1 - Показати всіх котів")
        print("2 - Знайти кота за ім'ям")
        print("3 - Оновити вік кота")
        print("4 - Додати особливість коту")
        print("5 - Видалити кота")
        print("6 - Видалити всіх котів")
        print("0 - Вихід")
        
        choice = input("\n🎯 Оберіть дію: ")
        
        if choice == '1':
            read_all()
        elif choice == '2':
            read_by_name()
        elif choice == '3':
            update_age()
        elif choice == '4':
            add_feature()
        elif choice == '5':
            delete_by_name()
        elif choice == '6':
            delete_all()
        elif choice == '0':
            print("👋 До побачення!")
            break
        else:
            print("❌ Невірний вибір")

# Оновлений кінець файлу
if __name__ == "__main__":
    print("✅ Підключення до MongoDB успішне!")
    print("\n🐱 СИСТЕМА УПРАВЛІННЯ КОТАМИ")
    print("=" * 40)
    
    
    try:
        # Додамо тестового кота
        if collection.count_documents({}) == 0:
            test_cat = {
                "name": "barsik",
                "age": 3,
                "features": ["ходить в капцях", "дає себе гладити", "рудий"]
            }
            collection.insert_one(test_cat)
            print("➕ Додано тестового кота Barsik")
        
        # Запускаємо меню
        main_menu()
    except Exception as e:
        print(f"❌ Критична помилка: {e}")
        print("💡 Перевірте підключення до MongoDB")