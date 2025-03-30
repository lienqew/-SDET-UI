import random
import string
import pytest
from selenium.webdriver.support.wait import WebDriverWait
from locators.all_locators import AbsolutelyAllLocators
from pages.add_customer_page import AddCustomerPage
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
import allure
from allure_commons.types import Severity


@allure.epic("Управление клиентами")
@allure.feature("Добавление клиентов")
class TestAddCustomer:
    @allure.story("Создание нового клиента")
    @allure.severity(Severity.BLOCKER)
    @allure.description("""
    Тест добавляет нового клиента в систему с автоматически сгенерированными данными.
    Проверяет корректность отображения сообщения об успешном создании.
    """)
    def test_add_customer(self, driver):
        with allure.step("Подготовка тестовых данных"):
            post_code = ''.join(random.choices(string.digits, k=10))
            first_name = ''.join(chr(int(digit) + ord('a')) for digit in post_code)

            allure.attach(f"Post Code: {post_code}", name="Тестовые данные",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Инициализация страницы"):
            add_customer_page = AddCustomerPage(
                driver,
                'https://www.globalsqa.com/angularJs-protractor/BankingProject/#/manager'
            )
            add_customer_page.open()
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Страница добавления клиента",
                attachment_type=allure.attachment_type.PNG
            )

        with allure.step("Заполнение формы"):
            add_customer_page.fill_customer_details(first_name, "Autotest", post_code)
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Форма после заполнения",
                attachment_type=allure.attachment_type.PNG
            )

        with allure.step("Отправка формы"):
            add_customer_page.submit()

            try:
                alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
                alert_text = alert.text
                alert.accept()
                allure.attach(
                    alert_text,
                    name="Текст алерта",
                    attachment_type=allure.attachment_type.TEXT
                )
                assert "Customer added successfully" in alert_text
            except Exception as e:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="Ошибка при отправке",
                    attachment_type=allure.attachment_type.PNG
                )
                pytest.fail(f"Не появилось сообщение об успехе: {str(e)}")

        allure.dynamic.title(f"Успешно добавлен клиент: {first_name}")
