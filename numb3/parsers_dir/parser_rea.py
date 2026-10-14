import os
import sys

# ---- ДОБАВЛЕНО: папка, где лежит этот файл (parsers_dir), в sys.path,
# чтобы import db_functions нашёл соседний файл ----
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
# ---------------------------------------------------

import requests as rq
from bs4 import BeautifulSoup
from datetime import datetime
import time
import db_functions as db
from urllib.parse import urljoin


# ============================================================
# Общие имена категорий — как в main.py
# ============================================================
CATEGORY_MAP = {
    "Наука":                      "Наука и инновации",
    "Спорт":                      "Спорт",
    "Абитуриентам":               "Абитуриентам",
    "В мире":                     "Объявления и события",
    "Образование":                "Образование",
    "Студенчество":               "Студенческая жизнь",
    "Международная деятельность": "Международная деятельность",
    "Проекты":                    "Сотрудничество и партнёрство",
    "Университет":                "Культура и творчество",
}

UNIVERSITY_NAME = "РЭУ"
FALLBACK_CATEGORY = "Без категории"

MAX_PAGES = 2
PER_PAGE = 12


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'Программа заняла: {end - start:.1f} сек; {(end - start) / 60:.2f} мин')
        print("=" * 100)
        return result
    return wrapper


# ============================================================
# Служебные функции
# ============================================================
def get_category_id(cursor, name):
    """category_id по имени; иначе — 'Без категории'; иначе — первая доступная."""
    row = cursor.execute(
        "SELECT category_id FROM news_categories WHERE name = ?", (name,)
    ).fetchone()
    if row is not None:
        return row[0]

    row = cursor.execute(
        "SELECT category_id FROM news_categories WHERE name = ?",
        (FALLBACK_CATEGORY,)
    ).fetchone()
    if row is not None:
        return row[0]

    row = cursor.execute(
        "SELECT category_id FROM news_categories ORDER BY category_id LIMIT 1"
    ).fetchone()
    return row[0] if row else None


def get_university_id(cursor, name):
    """Возвращает id вуза; создаёт с автоинкрементом, если нет."""
    row = cursor.execute(
        "SELECT university_id FROM universities WHERE name = ?", (name,)
    ).fetchone()
    if row is not None:
        return row[0]

    # вычисляем следующий свободный id (MAX + 1)
    row = cursor.execute(
        "SELECT COALESCE(MAX(university_id), 0) + 1 FROM universities"
    ).fetchone()
    new_id = row[0]

    cursor.execute(
        "INSERT INTO universities (university_id, name) VALUES (?, ?)",
        (new_id, name)
    )
    return new_id


def normalize_date(raw):
    """'15 сентября 2026' или 'Сегодня' → 'YYYY-MM-DD HH:MM:SS'."""
    if raw.strip() == "Сегодня":
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    months = {
        'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04',
        'мая': '05', 'июня': '06', 'июля': '07', 'августа': '08',
        'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12'
    }
    text = raw.strip().lower()
    for ru, num in months.items():
        text = text.replace(ru, num)

    for fmt in ('%d %m %Y', '%d.%m.%Y', '%Y-%m-%d'):
        try:
            dt = datetime.strptime(text, fmt)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
    return raw.strip()


# ============================================================
# Парсинг одного сайта
# ============================================================
@timer
def parse_all(con, cursor):
    print("Начинаем парсинг новостей РЭУ...")
    print("=" * 100)

    university_id = get_university_id(cursor, UNIVERSITY_NAME)
    con.commit()

    total_new = 0

    for i in range(1, MAX_PAGES + 1):
        url = f"https://www.rea.ru/news?tree-content-path=news&page={i}&per-page={PER_PAGE}"
        try:
            response = rq.get(url, timeout=10)
        except Exception as e:
            print(f"[SKIP] {url}: {e}")
            continue

        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.select('a.catalog__item-content')
        if not items:
            print(f"Страница {i} пуста, завершаем.")
            break

        for item in items:
            title_tag = item.select_one('.catalog__item-title')
            date_tag = item.select_one('.catalog__item-date')
            if title_tag is None or date_tag is None:
                continue

            link = urljoin("https://www.rea.ru", item.get("href")).split("?")[0]

            # пропускаем дубликаты
            if cursor.execute("SELECT 1 FROM news WHERE link = ?", (link,)).fetchone():
                continue

            try:
                sub = rq.get(link, timeout=10)
            except Exception as e:
                print(f"[SKIP] {link}: {e}")
                continue

            if sub.status_code != 200:
                continue

            soup_sub = BeautifulSoup(sub.text, 'html.parser')

            content_tag = soup_sub.select_one(".catalog-detail__text")
            content = content_tag.get_text(" ", strip=True) if content_tag else "no text"

            cat_tag = soup_sub.select_one("li.catalog-detail__tag")
            raw_cat = cat_tag.get_text(strip=True) if cat_tag else ""
            cat_name = CATEGORY_MAP.get(raw_cat, FALLBACK_CATEGORY)
            category_id = get_category_id(cursor, cat_name)

            date_text = normalize_date(date_tag.get_text(strip=True))
            title = title_tag.get_text(strip=True)

            ok = db.insert_news(
                con, cursor, title, date_text, link,
                category_id, university_id, content
            )
            if ok:
                total_new += 1

            time.sleep(0.2)

    print("=" * 100)
    print(f"Парсинг закончился, добавлено новых: {total_new}")
    return total_new


@timer
def check_news(con, cursor):
    """Проверяет только первую страницу — есть ли новая новость."""
    print("Проверяем наличие новых новостей...")

    url = "https://www.rea.ru/news?tree-content-path=news&page=1&per-page=12"
    try:
        response = rq.get(url, timeout=10)
    except Exception as e:
        print(f"[SKIP] {url}: {e}")
        return

    if response.status_code != 200:
        print(f"Ошибка: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    item = soup.select_one("a.catalog__item-content")
    if not item:
        print("Новости не найдены")
        return

    title_tag = item.select_one(".catalog__item-title")
    date_tag = item.select_one(".catalog__item-date")
    link = urljoin("https://www.rea.ru", item.get("href")).split("?")[0]
    title_text = title_tag.get_text(strip=True)

    print(f"Последняя новость на сайте: {title_text}")

    last = db.get_last_news(cursor)
    if last is None:
        print("БД пустая — парсим всё.")
        parse_all(con, cursor)
        return

    if title_text == last[0]:
        print("Новых новостей нет.")
        return

    print("Обнаружена новая новость!")

    try:
        sub = rq.get(link, timeout=10)
    except Exception as e:
        print(f"[SKIP] {link}: {e}")
        return

    soup_sub = BeautifulSoup(sub.text, "html.parser")

    content_tag = soup_sub.select_one(".catalog-detail__text")
    content = content_tag.get_text(" ", strip=True) if content_tag else "no text"

    cat_tag = soup_sub.select_one("li.catalog-detail__tag")
    raw_cat = cat_tag.get_text(strip=True) if cat_tag else ""
    cat_name = CATEGORY_MAP.get(raw_cat, FALLBACK_CATEGORY)
    category_id = get_category_id(cursor, cat_name)

    university_id = get_university_id(cursor, UNIVERSITY_NAME)

    date_text = normalize_date(date_tag.get_text(strip=True))

    db.insert_news(con, cursor, title_text, date_text, link,
                   category_id, university_id, content)


# ============================================================
# Точка входа БЕЗ аргументов — вызывается из main.py
# ============================================================
def parse():
    con, cursor = db.connect()
    try:
        db.table_news(con, cursor)
        db.table_categories(con, cursor)
        db.table_university(con, cursor)

        university_id = get_university_id(cursor, UNIVERSITY_NAME)
        con.commit()

        # проверяем, есть ли хоть одна новость РЭУ
        row = cursor.execute(
            "SELECT 1 FROM news WHERE university_id = ? LIMIT 1",
            (university_id,)
        ).fetchone()

        if row is None:
            print("Новостей РЭУ в базе нет — полный парсинг.")
            parse_all(con, cursor)
        else:
            check_news(con, cursor)
    finally:
        con.close()


if __name__ == "__main__":
    parse()