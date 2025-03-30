import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.all_locators import AbsolutelyAllLocators
from selenium.webdriver.common.by import By
import allure
from allure_commons.types import Severity


@allure.epic("Управление клиентами")
@allure.feature("Удаление клиентов")
@allure.tag("Регресс", "UI")
class TestCustomerDeletion:
    CUSTOMERS_URL = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/manager/list"

    @allure.story("Удаление клиентов по длине имени")
    @allure.severity(Severity.CRITICAL)
    @allure.description("""Тест удаляет всех клиентов, у которых длина имени ближе всего к средней длине всех имён""")
    def test_delete_all_closest_candidates(self, driver):
        with allure.step("Открытие страницы и загрузка данных"):
            driver.get(self.CUSTOMERS_URL)
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located(AbsolutelyAllLocators.customer_table))

            name_elements = driver.find_elements(*AbsolutelyAllLocators.first_name_cells)
            names = [name.text for name in name_elements if name.text not in ["First Name", ""]]

            allure.attach("\n".join(names), name="Исходный список клиентов", attachment_type=allure.attachment_type.TEXT)
            allure.attach(driver.get_screenshot_as_png(), name="Скриншот таблицы до удаления", attachment_type=allure.attachment_type.PNG)

        if not names:
            pytest.skip("Нет клиентов для удаления")

        with allure.step("Расчёт средней длины имён"):
            lengths = [len(name) for name in names]
            avg_length = sum(lengths) / len(lengths)

            calculation = (
                f"Общее количество клиентов: {len(names)}\n"
                f"Сумма длин имён: {sum(lengths)}\n"
                f"Средняя длина: {avg_length:.2f}"
            )
            allure.attach(calculation, name="Расчёт средней длины", attachment_type=allure.attachment_type.TEXT)

        with allure.step("3. Поиск кандидатов на удаление"):
            min_diff = min(abs(len(x) - avg_length) for x in names)
            closest_names = [name for name in names if abs(len(name) - avg_length) == min_diff]

            candidates_info = (
                f"Найдено кандидатов: {len(closest_names)}\n"
                f"Имена: {', '.join(closest_names)}\n"
                f"Длины: {[len(name) for name in closest_names]}"
            )
            allure.attach(candidates_info, name="Кандидаты на удаление", attachment_type=allure.attachment_type.TEXT)

        with allure.step("4. Процесс удаления"):
            rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
            deleted_count = 0

            for row in rows:
                try:
                    name = row.find_element(By.XPATH, ".//td[1]").text
                    if name in closest_names:
                        with allure.step(f"Удаление клиента: {name}"):
                            delete_btn = row.find_element(By.XPATH, ".//button[contains(., 'Delete')]")
                            delete_btn.click()
                            time.sleep(1)
                            deleted_count += 1

                            allure.attach(driver.get_screenshot_as_png(), name=f"После удаления {name}", attachment_type=allure.attachment_type.PNG)
                except Exception as e:
                    allure.attach(str(e), name=f"Ошибка при обработке строки", attachment_type=allure.attachment_type.TEXT)
                    continue

        with allure.step("5. Верификация результатов"):
            remaining_names = [
                name.text for name in driver.find_elements(*AbsolutelyAllLocators.first_name_cells)
                if name.text not in ["First Name", ""]
            ]

            result_check = (
                f"Удалено клиентов: {deleted_count} из {len(closest_names)}\n"
                f"Оставшиеся клиенты ({len(remaining_names)}):\n{', '.join(remaining_names)}"
            )
            allure.attach(result_check, name="Результаты удаления", attachment_type=allure.attachment_type.TEXT)

            # Основные проверки
            assert deleted_count == len(closest_names), "Удалены не все кандидаты"
            assert all(name not in remaining_names for name in closest_names), "Некоторые кандидаты остались в таблице"

            allure.attach(driver.get_screenshot_as_png(), name="Финальный скриншот таблицы", attachment_type=allure.attachment_type.PNG)

        allure.dynamic.title(f"Успешно удалено {deleted_count} клиентов из {len(closest_names)} кандидатов")
