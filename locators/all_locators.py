from selenium.webdriver.common.by import By


class AbsolutelyAllLocators:
    # Главные кнопки(вкладки)
    tab_button_add_customer = (By.XPATH, "//button[normalize-space()='Add Customer']")
    tab_button_customers = (By.XPATH, "//button[@ng-click='showCust()']")

    tab_button_open_account = (By.XPATH, "//button[contains(., 'Open Account')]")

    # Поля формы (после нажатия на Add Customer)
    first_name_field = (By.CSS_SELECTOR, "input[ng-model='fName']")
    last_name_field = (By.CSS_SELECTOR, "input[ng-model='lName']")
    post_code_field = (By.CSS_SELECTOR, "input[ng-model='postCd']")

    # Кнопка отправки
    add_customer_button = (By.XPATH, "//button[@type='submit']")

    # Таблица на вкладке Customers
    first_name_header = (By.XPATH, "//a[contains(@ng-click, 'fName')]")
    customer_table = (By.CLASS_NAME, "table-bordered")
    first_name_cells = (By.XPATH, "//table//td[1]") # Ячейки с именами
    customer_rows = (By.XPATH, "//table//tbody/tr")  # Все строки таблицы
    delete_buttons = (By.XPATH, "//table//button[contains(., 'Delete')]")  # Кнопки удаления
    # Элементы управления таблицей
    search_field = (By.XPATH, "//input[@ng-model='searchCustomer']")  # Поле поиска
