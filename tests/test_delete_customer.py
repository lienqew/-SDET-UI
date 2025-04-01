# Импорты из стандартной библиотеки
import pytest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Импорты сторонних библиотек
import allure
from allure_commons.types import Severity

# Импорты модулей текущего проекта
from pages.get_customer_page import CustomerPage
from config import Config


@allure.epic("Управление клиентами")
@allure.feature("Удаление клиентов")
class TestCustomerDeletion:
    @allure.story("Удаление клиентов на основе средней длины имени")
    @allure.severity(Severity.BLOCKER)
    @allure.description("Тест удаляет всех клиентов, у которых длина имени ближе всего к средней длине всех имён.")
    def test_delete_customers_by_average_length(self, driver):
        with allure.step("Открытие страницы клиентов"):
            customer_page = CustomerPage(driver, Config.BASE_URL + "/list")
            customer_page.open()

        with allure.step("Ожидание загрузки таблицы клиентов"):
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//table//td[1]")))

        with allure.step("Получение списка имен клиентов"):
            names = customer_page.get_customer_names()
            print("Список имен клиентов:", names)

            if not names:
                pytest.skip("Нет клиентов для удаления")

        with allure.step("Вычисление средней длины имен"):
            lengths = [len(name) for name in names if name not in ["First Name", ""]]
            average_length = sum(lengths) / len(lengths) if lengths else 0
            print("Средняя длина имен:", average_length)

        with allure.step("Поиск кандидатов на удаление"):
            min_diff = min(abs(len(name) - average_length) for name in names)
            closest_names = [name for name in names if abs(len(name) - average_length) == min_diff]
            print("Кандидаты на удаление:", closest_names)

        with allure.step("Удаление клиентов"):
            for closest_name in closest_names:
                customer_page.delete_customer(closest_name)

        with allure.step("Проверка, что клиенты были удалены"):
            remaining_names = customer_page.get_customer_names()
            assert all(name not in remaining_names for name in closest_names), f"Некоторые кандидаты остались: {closest_names}"
