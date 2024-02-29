from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import settings


class ChromeDriver:
    """Класс для работы с вебдрайверами Selenium."""

    def __init__(self):
        """Инициализировать объект класса Driver."""
        self.__chromedriver_path = settings.CHROMEDRIVER_PATH
        self.__driver = self.__initialize_driver()

    def __enter__(self):
        """Для менеджера контекста (with Driver() as *)"""
        return self.__driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Для менеджера контекста (with Driver() as *)"""
        self.__driver.close()
        self.__driver.quit()

    def get_driver(self):
        return self.__driver

    def __initialize_driver(self) -> webdriver:
        """Инициализировать драйвер с готовыми настройками.

        :return: драйвер с готовыми настройками.
        """
        options = webdriver.ChromeOptions()

        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
        })
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        service = Service(executable_path=self.__chromedriver_path)
        driver: webdriver = webdriver.Chrome(
            service=service,
            options=options
        )

        return driver
