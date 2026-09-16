import csv
from datetime import datetime
from collections import defaultdict

months_ru = {
    'January': 'Январь', 'February': 'Февраль', 'March': 'Март',
    'April': 'Апрель', 'May': 'Май', 'June': 'Июнь',
    'July': 'Июль', 'August': 'Август', 'September': 'Сентябрь',
    'October': 'Октябрь', 'November': 'Ноябрь', 'December': 'Декабрь'
}

monthly_count = defaultdict(int)

with open('mai_news.csv', 'r', encoding='utf-8', errors='ignore') as file:
    content = file.read()
    lines = content.splitlines()
    reader = csv.DictReader(lines)
    for row in reader:
        try:
            date_str = row['Дата']
            date_obj = datetime.strptime(date_str, '%d.%m.%Y')
            month_en = date_obj.strftime('%B')
            month_ru = months_ru.get(month_en, month_en)
            monthly_count[month_ru] += 1
        except:
            pass

print("\n" + "="*40)
print("СТАТИСТИКА ПО МЕСЯЦАМ (за все годы)")
print("="*40)
print(f"{'Месяц':<15} {'Количество новостей':<20}")
print("-"*40)
for month, count in sorted(monthly_count.items()):
    print(f"{month:<15} {count:<20}")
print("-"*40)
print(f"{'ИТОГО:':<15} {sum(monthly_count.values()):<20}")
print("="*40)