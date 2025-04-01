from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.add_customer_locators import AddCustomerLocators

class AddCustomerPage:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def open(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(AddCustomerLocators.TAB_BUTTON_ADD_CUSTOMER)).click()

    def fill_customer_details(self, first_name, last_name, post_code):
        def _fill_field(locator, value):
            field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))
            field.clear()
            field.send_keys(value)

        _fill_field(AddCustomerLocators.FIRST_NAME_FIELD, first_name)
        _fill_field(AddCustomerLocators.LAST_NAME_FIELD, last_name)
        _fill_field(AddCustomerLocators.POST_CODE_FIELD, post_code)

    def submit(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(AddCustomerLocators.ADD_CUSTOMER_BUTTON)).click()
