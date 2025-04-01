from selenium.webdriver.common.by import By


class CustomerPage:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def open(self):
        self.driver.get(self.url)

    def get_customer_names(self):
        # Получаем все имена из таблицы
        name_elements = self.driver.find_elements(By.XPATH, "//table//td[1]")
        return [element.text for element in name_elements]

    def delete_customer(self, name):
        # Находим строку с клиентом и нажимаем кнопку удаления
        rows = self.driver.find_elements(By.XPATH, "//table//tr")
        for row in rows:
            if name in row.text:
                delete_button = row.find_element(By.XPATH, ".//button[contains(text(), 'Delete')]")
                delete_button.click()
                break
