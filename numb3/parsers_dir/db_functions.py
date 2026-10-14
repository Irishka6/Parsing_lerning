import os
import sqlite3 as sql
from datetime import datetime


def _news_db_path():
    """Путь к news.db — рядом с main.py (на уровень выше parsers_dir)."""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(BASE_DIR, '..', 'news.db')


def connect():
    conn = sql.connect(_news_db_path())
    cursor = conn.cursor()
    return conn, cursor


def connect_users():
    conn = sql.connect("users.db")
    cursor = conn.cursor()
    return conn, cursor


def table_news(con, cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            link TEXT UNIQUE NOT NULL,
            published_date TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            university_id INTEGER NOT NULL,
            added_at TEXT DEFAULT (datetime('now')),
            content TEXT DEFAULT 'no text'
        );
    """)
    con.commit()


def table_categories(con, cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news_categories (
            category_id INTEGER NOT NULL,
            name TEXT NOT NULL
        );
    """)
    con.commit()


def table_university(con, cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS universities (
            university_id INTEGER NOT NULL,
            name TEXT NOT NULL
        );
    """)
    con.commit()


def table_users(con, cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_categories (
            user_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)
    con.commit()


def insert_news(con, cursor, title, published_date, link,
                category_id, university_id, content="no text"):
    cursor.execute("""
        INSERT OR IGNORE INTO news
            (title, link, published_date, category_id, university_id, added_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        title, link, published_date, category_id, university_id,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    con.commit()
    if cursor.rowcount == 1:
        print(f"[INSERT] {title}")
        return True
    return False


def view_data(cursor):
    data = cursor.execute("SELECT * FROM news")
    row_count = cursor.execute("SELECT COUNT(*) FROM news").fetchone()[0]
    return data, row_count


def truncate_table(con, cursor):
    cursor.execute("DELETE FROM news")
    con.commit()


def get_last_news(cursor):
    """Возвращает (title,) последней добавленной новости или None."""
    cursor.execute("""
        SELECT title
        FROM news
        ORDER BY published_date DESC, id DESC
        LIMIT 1
    """)
    return cursor.fetchone()


def truncate(con, cursor, table_name):
    cursor.execute(f"DELETE FROM {table_name}")
    con.commit()
    print(f"Таблица {table_name} очищена")


if __name__ == "__main__":
    con_n, cursor_n = connect()
    truncate_table(con_n, cursor_n)