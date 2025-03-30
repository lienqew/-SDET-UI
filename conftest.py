import os
import pytest
import allure
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function")
def driver(request):
    """Фикстура драйвера с поддержкой параллельного выполнения"""
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "default")
    current_dir = os.path.abspath(os.getcwd())
    temp_dir = os.path.join(current_dir, f"tmp_test_{worker_id}_{uuid.uuid4()}")

    # Настройки Chrome для параллельного запуска
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Инициализация драйвера
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    yield driver

    # Завершение работы
    try:
        if driver:
            # Делаем финальный скриншот
            allure.attach(
                driver.get_screenshot_as_png(),
                name="final_state",
                attachment_type=allure.attachment_type.PNG
            )
            driver.quit()

            # Удаляем временную папку
            try:
                os.rmdir(temp_dir)
            except Exception as e:
                print(f"Ошибка при удалении временной папки: {str(e)}")
    except Exception as e:
        allure.attach(
            str(e),
            name="teardown_error",
            attachment_type=allure.attachment_type.TEXT
        )
