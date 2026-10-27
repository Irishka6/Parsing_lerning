import sys
from pathlib import Path
import pytest
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
sys.path.append(str(Path(__file__).parent.parent))
from pages.base_page import GeometryCalculator


def load_test_data():
    """Читает данные из JSON файла."""
    json_path = Path(__file__).parent / '..' / 'data' / 'percent_cases.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)





@pytest.fixture
def calc_page():
    options = Options()
    options.add_argument('--headless')  # Запуск без интерфейса

    service = Service(executable_path=r"D:\yandexdriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    page = GeometryCalculator(driver).open()
    yield page

    driver.quit()


@pytest.mark.parametrize("test_case", load_test_data())
def test_geometry_calculations(calc_page, test_case):
    figure_name = list(test_case.keys())[0]
    params = test_case[figure_name]
    expected_value = params.pop("expected")

    methods_map = {
        "Square Area": calc_page.square_area,
        "Rectangle Area": calc_page.rectangle_area,
        "Circle Area": calc_page.circle_area,
        "Cube Volume": calc_page.cube_volume,
        "Box Volume": calc_page.box_volume,
        "Cylinder Volume": calc_page.cylinder_volume
    }

    if figure_name not in methods_map:
        pytest.fail(f"Метод для фигуры '{figure_name}' не найден в methods_map")

    # Получаем результат с экрана в виде строки
    actual_str = methods_map[figure_name](**params)
    expected_str = str(expected_value)

    try:
        # Нормализуем данные: заменяем запятые на точки (локаль) и убираем пробелы
        actual_float = float(actual_str.replace(',', '.').replace(' ', ''))
        expected_float = float(expected_str.replace(',', '.').replace(' ', ''))

        # Сравниваем числа с допустимой погрешностью (rel=1e-5 позволяет игнорировать мелкую разницу в округлении)
        assert actual_float == pytest.approx(expected_float, rel=1e-5), \
            f"Для '{figure_name}' ожидалось {expected_float}, но получено {actual_float}"

    except ValueError:
        # Fallback для негативных тестов (когда ожидается и возвращается текст ошибки, а не число)
        assert actual_str == expected_str, \
            f"Для '{figure_name}' ожидался текст '{expected_str}', но получено '{actual_str}'"