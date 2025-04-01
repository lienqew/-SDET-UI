from selenium.webdriver.common.by import By


class AddCustomerLocators:
    # Главные кнопки (вкладки)
    TAB_BUTTON_ADD_CUSTOMER = (By.XPATH, "//button[normalize-space()='Add Customer']")

    # Поля формы (после нажатия на Add Customer)
    FIRST_NAME_FIELD = (By.CSS_SELECTOR, "input[ng-model='fName']")
    LAST_NAME_FIELD = (By.CSS_SELECTOR, "input[ng-model='lName']")
    POST_CODE_FIELD = (By.CSS_SELECTOR, "input[ng-model='postCd']")

    # Кнопка отправки
    ADD_CUSTOMER_BUTTON = (By.XPATH, "//button[@type='submit']")