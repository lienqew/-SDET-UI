from selenium.webdriver.common.by import By


class CustomerLocators:
    # Таблица на вкладке Customers
    CUSTOMER_TABLE = (By.CLASS_NAME, "table-bordered")
    FIRST_NAME_CELLS = (By.XPATH, "//table//td[1]")  # Ячейки с именами
    DELETE_BUTTONS = (By.XPATH, "//table//button[contains(., 'Delete')]")  # Кнопки удаления
    SEARCH_FIELD = (By.XPATH, "//input[@ng-model='searchCustomer']")  # Поле поиска
