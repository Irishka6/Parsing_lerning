from pages.percent_calculator_page import PercentCalculatorPage

class GeometryCalculator(PercentCalculatorPage):
    """Дочерний класс для геометрических вычислений, наследующий все кнопки."""

    def _enter_number(self, number):
        """Вспомогательный метод для посимвольного ввода чисел."""
        for char in str(number):
            if char == '0': self.click_0()
            elif char == '1': self.click_1()
            elif char == '2': self.click_2()
            elif char == '3': self.click_3()
            elif char == '4': self.click_4()
            elif char == '5': self.click_5()
            elif char == '6': self.click_6()
            elif char == '7': self.click_7()
            elif char == '8': self.click_8()
            elif char == '9': self.click_9()
            elif char == '.': self.click_dot()
        return self

    # --- 1. ПЛОЩАДЬ КВАДРАТА (S = a^2) ---
    def square_area(self, a):
        self._enter_number(a)
        self.click_square()
        self.click_enter()
        return self.get_result()

    # --- 2. ПЛОЩАДЬ ПРЯМОУГОЛЬНИКА (S = a * b) ---
    def rectangle_area(self, a, b):
        self._enter_number(a)
        self.click_multiply()
        self._enter_number(b)
        self.click_enter()
        return self.get_result()

    # --- 3. ПЛОЩАДЬ КРУГА (S = π * r^2) ---
    def circle_area(self, radius):
        self.click_pi()
        self.click_multiply()
        self._enter_number(radius)
        self.click_square()
        self.click_enter()
        return self.get_result()

    # --- 4. ОБЪЕМ КУБА (V = a^3) ---
    def cube_volume(self, a):
        self._enter_number(a)
        self.click_power()
        self.click_3()
        self.click_enter()
        return self.get_result()

    # --- 5. ОБЪЕМ ПРЯМОУГОЛЬНОГО ПАРАЛЛЕЛЕПИПЕДА (V = a * b * c) ---
    def box_volume(self, a, b, c):
        self._enter_number(a)
        self.click_multiply()
        self._enter_number(b)
        self.click_multiply()
        self._enter_number(c)
        self.click_enter()
        return self.get_result()

    # --- 6. ОБЪЕМ ЦИЛИНДРА (V = π * r^2 * h) ---
    def cylinder_volume(self, radius, height):
        self.click_pi()
        self.click_multiply()
        self._enter_number(radius)
        self.click_square()
        self.click_multiply()
        self._enter_number(height)
        self.click_enter()
        return self.get_result()