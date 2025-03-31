import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.all_locators import AbsolutelyAllLocators
import allure
from allure_commons.types import Severity


@allure.epic("Управление клиентами")
@allure.feature("Сортировка клиентов")
class TestCustomerSorting:
    CUSTOMERS_URL = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/manager/list"

    @allure.story("Сортировка по имени")
    @allure.severity(Severity.NORMAL)
    @allure.description("""Проверка сортировки клиентов по имени через двойной клик по first name. Первый кклик - сортировка Z-A, второй - A-Z""")
    def test_sort_customers_by_name(self, driver):
        with allure.step("Переход на страницу клиентов"):
            driver.get(self.CUSTOMERS_URL)
            allure.attach(driver.get_screenshot_as_png(), name="Исходное состояние таблицы", attachment_type=allure.attachment_type.PNG)

        with allure.step("Ожидание загрузки таблицы"):
            try:
                WebDriverWait(driver, 15).until(EC.visibility_of_element_located(AbsolutelyAllLocators.customer_table))
            except Exception as e:
                allure.attach(driver.page_source, name="Page source", attachment_type=allure.attachment_type.HTML)
                pytest.fail(f"Таблица не загрузилась: {str(e)}")

        with allure.step("Получение исходного порядка имен"):
            initial_names = [el.text for el in driver.find_elements(*AbsolutelyAllLocators.first_name_cells)[1:]]
            allure.attach("\n".join(initial_names), name="Исходный порядок", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Выполнение двойной сортировки"):
            header = driver.find_element(*AbsolutelyAllLocators.first_name_header)

            # Первый клик (Z-A)
            header.click()
            time.sleep(1)
            allure.attach(driver.get_screenshot_as_png(), name="После первого клика (Z-A)", attachment_type=allure.attachment_type.PNG)

            # Второй клик (A-Z)
            header.click()
            time.sleep(1)
            allure.attach(driver.get_screenshot_as_png(), name="После второго клика (A-Z)", attachment_type=allure.attachment_type.PNG)

        with allure.step("Проверка результата"):
            sorted_names = [el.text for el in driver.find_elements(*AbsolutelyAllLocators.first_name_cells)[1:]]
            allure.attach("\n".join(sorted_names), name="Отсортированный порядок", attachment_type=allure.attachment_type.TEXT)

            assert sorted_names == sorted(initial_names), "Сортировка A-Z не работает"

        allure.dynamic.title("Сортировка по имени выполнена успешно")
