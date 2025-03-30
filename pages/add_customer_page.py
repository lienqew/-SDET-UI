from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from locators.all_locators import AbsolutelyAllLocators


class AddCustomerPage:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def open(self):
        self.driver.get(self.url)
        # Добавляем ожидание кнопки
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(AbsolutelyAllLocators.tab_button_add_customer)).click()

    def fill_customer_details(self, first_name, last_name, post_code):
        # Ожидаем и заполняем поля (сохраняем вашу логику)
        def _fill_field(locator, value):
            field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))
            field.clear()
            field.send_keys(value)

        _fill_field(AbsolutelyAllLocators.first_name_field, first_name)
        _fill_field(AbsolutelyAllLocators.last_name_field, last_name)
        _fill_field(AbsolutelyAllLocators.post_code_field, post_code)

    def submit(self):
        # Ожидаем кнопку перед кликом
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(AbsolutelyAllLocators.add_customer_button)).click()
