import sqlite3
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from collections import defaultdict

connection = sqlite3.connect('monitoring.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Users(
    id INT PRIMARY KEY,
    head TEXT,
    date TEXT,
    http TEXT,
    timeficks TEXT,
    category TEXT);
    ''')

url = 'https://media.kpfu.ru/news?kn%5B0%5D=Международное%20сотрудничество&created='
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

while True:
    if page == 1:
        current_url = 'https://media.kpfu.ru/news?kn%5B0%5D=Международное%20сотрудничество&created='

    if page > 1:
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
        break

    for new in news:
        # --- ДОБАВЛЕНО: защита от None ---
        link_tag = new.select_one('.boldLink')
        date_tag_elem = new.select_one('.newsItem-date')
        if not link_tag or not date_tag_elem:
            continue
        # ---------------------------------

        htt = 'https://media.kpfu.ru/news?kn%5B0%5D=Международное%20сотрудничество&created=' + link_tag.get('href')
        title_tag = link_tag.text.strip()
        date_tag = date_tag_elem.text.strip()
        print(htt, title_tag, date_tag)
        writer.writerow([htt, title_tag, date_tag])

        # --- ДОБАВЛЕНО: сохраняем в список для docx ---
        all_news_data.append({'link': htt, 'title': title_tag, 'date': date_tag})
        # -----------------------------------------------

        try:
            date_obj = datetime.strptime(date_tag, '%d.%m.%Y')
            month_key = date_obj.strftime('%B %Y')
            monthly_count[month_key] += 1
        except:
            pass

    # --- ДОБАВЛЕНО: защита от None у кнопки "next" ---
    next_btn = soup.select_one('.pager__item.pager__item--next a')
    last_btn = soup.select_one('.pager__item.pager__item--last a')
    if not next_btn or not last_btn:
        break
    # -------------------------------------------------

    current_url = 'https://media.kpfu.ru/news?kn%5B0%5D=Международное%20сотрудничество&created=' + next_btn.get('href')
    print(current_url)
    if current_url == soup.select_one('.pager__item.pager__item--last a').get('href'):
        break
    page += 1

connection.close()