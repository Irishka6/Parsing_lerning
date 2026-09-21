import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
import time


url = 'https://media.kpfu.ru/news?kn%5B0%5D=Международное%20сотрудничество&created='


# --- Подключение к БД ---
while True:
    connection = sqlite3.connect('monitoring.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        head TEXT,
        date TEXT,
        http TEXT,
        timeficks TEXT,
        category TEXT);
        ''')
    MAX_PAGES = 10
    INTERVAL = 60
    page = 1
    monthly_count = defaultdict(int)



    while page <= MAX_PAGES:
        if page == 1:
            current_url = 'https://media.kpfu.ru/news?kn%5B0%5D=Международное%20сотрудничество&created='
        try:
            response = requests.get(current_url, timeout=10)
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса (страница {page}): {e}")
            print("Прерываем парсинг, переходим к отчёту...")
            break

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        news = soup.select('.newsItem')

        if not news:
            print(f"Страница {page} пуста, завершаем.")
            break

        for new in news:
            link_tag = new.select_one('.boldLink')
            date_tag_elem = new.select_one('.newsItem-date')
            if not link_tag or not date_tag_elem:
                continue

            htt = 'https://media.kpfu.ru/news?kn%5B0%5D=Международное%20сотрудничество&created=' + link_tag.get('href')
            title_tag = link_tag.text.strip()
            date_tag = date_tag_elem.text.strip()
            now = datetime.now().strftime('%d.%m.%Y %H:%M')
            print(htt, title_tag, date_tag)

            # --- Запись в БД (с защитой от дублей) ---
            cursor.execute('SELECT 1 FROM Users WHERE http = ?', (htt,))
            if cursor.fetchone() is None:
                cursor.execute(
                    'INSERT INTO Users(head, date, http, timeficks, category) VALUES (?, ?, ?, ?, ?)',
                    (title_tag, date_tag, htt, now, 'Международное сотрудничество')
                )

            # --- Статистика по месяцам ---
            try:
                date_obj = datetime.strptime(date_tag, '%d.%m.%Y')
                month_key = date_obj.strftime('%B %Y')
                monthly_count[month_key] += 1
            except:
                pass

        # --- Пагинация ---
        next_btn = soup.select_one('.pager__item.pager__item--next a')
        if not next_btn:
            print("Кнопка 'Следующая' не найдена, завершаем.")
            break

        current_url = 'https://media.kpfu.ru/news?kn%5B0%5D=Международное%20сотрудничество&created=' + next_btn.get('href')
        print(f"--> Переход на страницу {page + 1}: {current_url}")
        page += 1

    print(f"\nОбработано страниц: {page}")

    # --- Сохраняем изменения и закрываем БД ---
    connection.commit()
    connection.close()
    print("Данные записаны в monitoring.db")
    time.sleep(INTERVAL)

# --- Статистика по месяцам ---
print("\n" + "=" * 50)
print("СТАТИСТИКА ПО МЕСЯЦАМ")
print("=" * 50)
print(f"{'Месяц':<20} {'Количество новостей':<20}")
print("-" * 50)
for month, count in sorted(monthly_count.items(), key=lambda x: datetime.strptime(x[0], '%B %Y')):
    print(f"{month:<20} {count:<20}")
print("-" * 50)
print(f"{'ИТОГО:':<20} {sum(monthly_count.values()):<20}")
print("=" * 50)
