# db_config.py
import psycopg2

def get_postgres_connection():
    """🔌 Підключення до службової БД postgres"""
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="postgres",  # службова БД
        user="postgres",
        password="567234"
    )

def get_task_management_connection():
    """🔌 Підключення до БД task_management"""
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="task_management",  # наша БД
        user="postgres",
        password="567234"
    )

def get_db_cursor(conn):
    """👤 Створення курсора"""
    return conn.cursor()