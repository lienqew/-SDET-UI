# Импорты из стандартной библиотеки
import pytest
import allure
from allure_commons.types import Severity
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Импорты модулей текущего проекта
from pages.add_customer_page import AddCustomerPage
from data.customer_data import CustomerDataGenerator
from config import Config


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
            first_name, last_name, post_code = CustomerDataGenerator.generate_customer_data()
            allure.attach(f"Post Code: {post_code}", name="Тестовые данные",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Инициализация страницы"):
            add_customer_page = AddCustomerPage(driver, Config.ADD_CUSTOMER_URL)
            add_customer_page.open()
            allure.attach(driver.get_screenshot_as_png(), name="Страница добавления клиента",
                          attachment_type=allure.attachment_type.PNG)

        with allure.step("Заполнение формы"):
            add_customer_page.fill_customer_details(first_name, last_name, post_code)
            allure.attach(driver.get_screenshot_as_png(), name="Форма после заполнения",
                          attachment_type=allure.attachment_type.PNG)

        with allure.step("Отправка формы"):
            add_customer_page.submit()

            try:
                # Ожидание появления алерта
                WebDriverWait(driver, 5).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert_text = alert.text
                alert.accept()  # Закрываем алерт
                allure.attach(alert_text, name="Текст алерта", attachment_type=allure.attachment_type.TEXT)
                assert "Customer added successfully" in alert_text
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Ошибка при отправке",
                              attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Не появилось сообщение об успехе: {str(e)}")

        allure.dynamic.title(f"Успешно добавлен клиент: {first_name}")
