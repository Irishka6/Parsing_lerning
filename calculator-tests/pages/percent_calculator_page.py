from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class PercentCalculatorPage:
    URL = "https://www.desmos.com/scientific?lang=ru"

    btn_0 = (By.CSS_SELECTOR, "[dcg-command='0']")
    btn_1 = (By.CSS_SELECTOR, "[dcg-command='1']")
    btn_2 = (By.CSS_SELECTOR, "[dcg-command='2']")
    btn_3 = (By.CSS_SELECTOR, "[dcg-command='3']")
    btn_4 = (By.CSS_SELECTOR, "[dcg-command='4']")
    btn_5 = (By.CSS_SELECTOR, "[dcg-command='5']")
    btn_6 = (By.CSS_SELECTOR, "[dcg-command='6']")
    btn_7 = (By.CSS_SELECTOR, "[dcg-command='7']")
    btn_8 = (By.CSS_SELECTOR, "[dcg-command='8']")
    btn_9 = (By.CSS_SELECTOR, "[dcg-command='9']")
    btn_square = (By.CSS_SELECTOR, "[dcg-command='a^2']")
    btn_power = (By.CSS_SELECTOR, "[dcg-command='a^b']")  # Степень (a в степени b)
    btn_abs = (By.CSS_SELECTOR, "[dcg-command='|a|']")  # Модуль (абсолютное значение)
    btn_sqrt = (By.CSS_SELECTOR, "[dcg-command='sqrt']")  # Квадратный корень
    btn_nthroot = (By.CSS_SELECTOR, "[dcg-command='nthroot']")  # Корень n-ой степени
    btn_pi = (By.CSS_SELECTOR, "[dcg-command='pi']")  # Число Пи
    btn_sin = (By.CSS_SELECTOR, "[dcg-command='sin']")  # Синус
    btn_cos = (By.CSS_SELECTOR, "[dcg-command='cos']")  # Косинус
    btn_tan = (By.CSS_SELECTOR, "[dcg-command='tan']")  # Тангенс
    btn_left_paren = (By.CSS_SELECTOR, "[dcg-command='(']")  # Левая скобка
    btn_right_paren = (By.CSS_SELECTOR, "[dcg-command=')']")  # Правая скобка
    btn_comma = (By.CSS_SELECTOR, "[dcg-command=',']")  # Запятая
    btn_divide = (By.CSS_SELECTOR, "[dcg-command='/']")  # Деление
    btn_multiply = (By.CSS_SELECTOR, "[dcg-command='*']")  # Умножение
    btn_minus = (By.CSS_SELECTOR, "[dcg-command='-']")  # Вычитание
    btn_dot = (By.CSS_SELECTOR, "[dcg-command='.']")  # Десятичная точка
    btn_ans = (By.CSS_SELECTOR, "[dcg-command='ans']")  # Последний ответ
    btn_plus = (By.CSS_SELECTOR, "[dcg-command='+']")  # Сложение
    btn_percent = (By.CSS_SELECTOR, "[dcg-command='%']")  # Процент
    btn_fraction = (By.CSS_SELECTOR, "[dcg-command='a/b']")  # Дробь

    result_field = (By.CSS_SELECTOR, ".dcg-mq-root-block.dcg-mq-show-grouping")
    btn_enter = (By.CSS_SELECTOR, "[dcg-command='enter']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)
        self.wait.until(EC.element_to_be_clickable(self.btn_2))
        return self

    def click_0(self):
        """Кликает по кнопке '0' на виртуальном калькуляторе."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_0))
        button.click()
        return self

    def click_1(self):
        """Кликает по кнопке '1' на виртуальном калькуляторе."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_1))
        button.click()
        return self

    def click_2(self):
        """Кликает по кнопке '2' на виртуальном калькуляторе."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_2))
        button.click()
        return self

    def click_3(self):
        """Кликает по кнопке '3' на виртуальном калькуляторе."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_3))
        button.click()
        return self

    def click_4(self):
        """Кликает по кнопке '4' на виртуальном калькуляторе."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_4))
        button.click()
        return self

    def click_5(self):
        """Кликает по кнопке '5' на виртуальном калькуляторе."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_5))
        button.click()
        return self

    def click_6(self):
        """Кликает по кнопке '6' на виртуальном калькуляторе."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_6))
        button.click()
        return self

    def click_7(self):
        """Кликает по кнопке '7' на виртуальном калькуляторе."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_7))
        button.click()
        return self

    def click_8(self):
        """Кликает по кнопке '8' на виртуальном калькуляторе."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_8))
        button.click()
        return self

    def click_9(self):
        """Кликает по кнопке '9' на виртуальном калькуляторе."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_9))
        button.click()
        return self

    def click_power(self):
        """Кликает по кнопке 'Степень (a^b)'."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_power))
        button.click()
        return self

    def click_abs(self):
        """Кликает по кнопке 'Модуль (|a|)'."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_abs))
        button.click()
        return self

    def click_sqrt(self):
        """Кликает по кнопке 'Квадратный корень'."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_sqrt))
        button.click()
        return self

    def click_nthroot(self):
        """Кликает по кнопке 'Корень n-ой степени'."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_nthroot))
        button.click()
        return self

    def click_pi(self):
        """Кликает по кнопке 'Пи'."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_pi))
        button.click()
        return self

    def click_sin(self):
        """Кликает по кнопке 'Синус (sin)'."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_sin))
        button.click()
        return self

    def click_cos(self):
        """Кликает по кнопке 'Косинус (cos)'."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_cos))
        button.click()
        return self

    def click_tan(self):
        """Кликает по кнопке 'Тангенс (tan)'."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_tan))
        button.click()
        return self

    def click_left_paren(self):
        """Кликает по левой скобке '('."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_left_paren))
        button.click()
        return self

    def click_right_paren(self):
        """Кликает по правой скобке ')'."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_right_paren))
        button.click()
        return self

    def click_comma(self):
        """Кликает по запятой ','."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_comma))
        button.click()
        return self

    def click_divide(self):
        """Кликает по кнопке 'Деление (/)'."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_divide))
        button.click()
        return self

    def click_multiply(self):
        """Кликает по кнопке 'Умножение (*)'."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_multiply))
        button.click()
        return self

    def click_minus(self):
        """Кликает по кнопке 'Вычитание (-)'."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_minus))
        button.click()
        return self

    def click_dot(self):
        """Кликает по кнопке 'Десятичная точка (.)'."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_dot))
        button.click()
        return self

    def click_ans(self):
        """Кликает по кнопке 'Последний ответ (ans)'."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_ans))
        button.click()
        return self

    def click_plus(self):
        """Кликает по кнопке 'Сложение (+)'."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_plus))
        button.click()
        return self

    def click_percent(self):
        """Кликает по кнопке 'Процент (%)'."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_percent))
        button.click()
        return self

    def click_fraction(self):
        """Кликает по кнопке 'Дробь (a/b)'."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_fraction))
        button.click()
        return self

    def click_square(self):
        button = self.wait.until(EC.element_to_be_clickable(self.btn_square))
        button.click()
        return self

    def click_enter(self):
        """Кликает по кнопке 'Enter' (ввод)."""
        button = self.wait.until(EC.element_to_be_clickable(self.btn_enter))
        button.click()
        return self

    def get_result(self) -> str:
        """Возвращает текст результата с экрана."""
        element = self.wait.until(EC.visibility_of_element_located(self.result_field))
        return element.text.strip()[1:]

