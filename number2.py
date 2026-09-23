import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from collections import defaultdict
import time


url = 'https://media.kpfu.ru/news?kn%5B0%5D=Международное%20сотрудничество&created='



while 1:
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
    INTERVAL = 30
    page = 1
    monthly_count = defaultdict(int)
    duplicate_found = 0


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


            cursor.execute('SELECT 1 FROM Users WHERE http = ?', (htt,))
            if cursor.fetchone() is None:
                cursor.execute(
                    'INSERT INTO Users(head, date, http, timeficks, category) VALUES (?, ?, ?, ?, ?)',
                    (title_tag, date_tag, htt, now, 'Международное сотрудничество')
                )
                print('Найдена новая новость: ', htt, title_tag, date_tag)
            else:
                duplicate_found = 1
                break
            try:
                date_obj = datetime.strptime(date_tag, '%d.%m.%Y')
                month_key = date_obj.strftime('%B %Y')
                monthly_count[month_key] += 1
            except:
                pass
        if duplicate_found:
            break
        next_btn = soup.select_one('.pager__item.pager__item--next a')
        if not next_btn:
            print("Кнопка 'Следующая' не найдена, завершаем.")
            break

        current_url = 'https://media.kpfu.ru/news?kn%5B0%5D=Международное%20сотрудничество&created=' + next_btn.get('href')
        print(f"--> Переход на страницу {page + 1}: {current_url}")
        page += 1

    print(f"\nОбработано страниц: {page}")

    connection.commit()
    connection.close()
    print("Данные записаны в monitoring.db")
    time.sleep(INTERVAL)
