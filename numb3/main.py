import json
import os
import importlib.util
import sqlite3
import time
import traceback
from datetime import datetime


# ============================================================
# Конфиг
# ============================================================
def load_config(path: str = 'config.json') -> dict:
    """Читает config.json рядом с main.py и делает пути абсолютными."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, path)

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Конфиг не найден: {config_path}")

    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    for key in ('news_db', 'users_db', 'output_file', 'parsers_dir'):
        if key in config and not os.path.isabs(config[key]):
            config[key] = os.path.join(base_dir, config[key])

    return config


# ============================================================
# Запуск парсеров
# ============================================================
def run_parse_in_all_py(directory: str, sleep_con: float = 0):
    """
    Находит все .py файлы в directory и запускает в каждом функцию parse().
    Пропускает main.py и файлы без parse().
    """
    me = os.path.basename(__file__)
    print(f"[DIR] Сканирую: {directory}")

    if not os.path.isdir(directory):
        print(f"[ERROR] Не папка: {directory}")
        return

    found = 0
    for root, _, files in os.walk(directory):
        for filename in files:
            if not filename.endswith('.py'):
                continue
            if filename == me:                          # не запускать самого себя
                continue

            filepath = os.path.join(root, filename)
            found += 1

            spec = importlib.util.spec_from_file_location(filename[:-3], filepath)
            if spec is None or spec.loader is None:
                print(f"[SKIP] Не удалось загрузить {filepath}")
                continue

            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
            except Exception as e:
                print(f"[ERROR] Ошибка при импорте {filepath}: {e}")
                continue

            parse_func = getattr(module, 'parse', None)
            if not callable(parse_func):
                print(f"[SKIP] В {filepath} нет функции parse()")
                continue

            print(f"[RUN] {filepath} → parse()")
            try:
                parse_func()                            # ← без аргументов
                print(f"[OK]  {filepath}")
            except Exception as e:
                print(f"[FAIL] {filepath}: {e}")
                traceback.print_exc()

            if sleep_con:
                time.sleep(sleep_con)

    if found == 0:
        print(f"[WARN] В {directory} не найдено .py файлов")


# ============================================================
# БД пользователей
# ============================================================
def init_users_db(name_bd="users.db"):
    connection = sqlite3.connect(name_bd)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_categories (
            user_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    ''')

    connection.commit()
    return connection, cursor


# ============================================================
# БД новостей
# ============================================================
def init_news_db(all_category, DEFAULT_UNIVERSITY_ID=1,
                 DEFAULT_UNIVERSITY="КФУ", name_bd="news.db"):
    connection = sqlite3.connect(name_bd)
    cursor = connection.cursor()
    CATEGORY_ID = {name: i for i, name in enumerate(all_category, start=1)}

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news_categories (
            category_id INTEGER NOT NULL,
            name TEXT NOT NULL
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS universities (
            university_id INTEGER NOT NULL,
            name TEXT NOT NULL
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            link TEXT UNIQUE NOT NULL,
            published_date TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            university_id INTEGER NOT NULL,
            added_at TEXT DEFAULT (datetime('now'))
        );
    ''')

    for name in all_category:
        cursor.execute('SELECT 1 FROM news_categories WHERE category_id = ?', (CATEGORY_ID[name],))
        if cursor.fetchone() is None:
            cursor.execute(
                'INSERT INTO news_categories (category_id, name) VALUES (?, ?)',
                (CATEGORY_ID[name], name)
            )

    cursor.execute('SELECT 1 FROM universities WHERE university_id = ?', (DEFAULT_UNIVERSITY_ID,))
    if cursor.fetchone() is None:
        cursor.execute(
            'INSERT INTO universities (university_id, name) VALUES (?, ?)',
            (DEFAULT_UNIVERSITY_ID, DEFAULT_UNIVERSITY)
        )

    connection.commit()
    return connection, cursor


# ============================================================
# Формирование send_list.txt
# ============================================================
def write_send_list(path: str, distribution: dict):
    """
    distribution: {user_id: [news_id1, news_id2, ...]}
    """
    written = 0
    with open(path, 'w', encoding='utf-8') as f:
        for user_id in sorted(distribution.keys()):
            news_ids = distribution[user_id]
            line = f"{user_id}: " + ", ".join(str(n) for n in news_ids)
            f.write(line + "\n")
            written += 1
    print(f"[SEND_LIST] {path}: записано {written} строк")


def get_news_for_user(news_cursor, user_cursor, user_id):
    """
    Возвращает список news_id, у которых category_id входит
    в категории, отслеживаемые пользователем.
    """
    user_cursor.execute(
        'SELECT category_id FROM user_categories WHERE user_id = ?', (user_id,)
    )
    cats = [row[0] for row in user_cursor.fetchall()]
    if not cats:
        return []

    placeholders = ','.join('?' for _ in cats)
    news_cursor.execute(
        f'SELECT id FROM news WHERE category_id IN ({placeholders})',
        cats
    )
    return [row[0] for row in news_cursor.fetchall()]


def build_send_list(news_cursor, user_cursor, output_file):
    user_cursor.execute('SELECT id FROM users')
    user_ids = [row[0] for row in user_cursor.fetchall()]

    distribution = {}
    for user_id in user_ids:
        distribution[user_id] = get_news_for_user(news_cursor, user_cursor, user_id)

    write_send_list(output_file, distribution)


# ============================================================
# main + периодический запуск
# ============================================================
def run_one_cycle(config, news_cursor, user_cursor):
    print(f"\n{'=' * 60}")
    print(f"[CYCLE] {datetime.now():%Y-%m-%d %H:%M:%S}")
    print('=' * 60)

    # 1. парсеры (каждый откроет news.db и запишет данные)
    run_parse_in_all_py(config["parsers_dir"])

    # 2. формируем send_list.txt
    build_send_list(news_cursor, user_cursor, config["output_file"])


def main(config):
    # инициализация обеих БД
    news_conn, news_cursor = init_news_db(config["all_category"],
                                          name_bd=config["news_db"])
    users_conn, users_cursor = init_users_db(name_bd=config["users_db"])

    interval_sec = int(config["interval_minutes"]) * 60

    try:
        while True:
            run_one_cycle(config, news_cursor, users_cursor)
            print(f"[SLEEP] Ждём {config['interval_minutes']} мин...")
            time.sleep(interval_sec)
    except KeyboardInterrupt:
        print("\n[STOP] Остановлено пользователем (Ctrl+C)")
    finally:
        news_conn.close()
        users_conn.close()
        print("[CLOSE] Соединения с БД закрыты")


if __name__ == '__main__':
    main(load_config())