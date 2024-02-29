from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import settings
from selenium.webdriver.firefox.service import Service
from fake_useragent import UserAgent


class FirefoxDriver:
    def __init__(self):
        self.__geckodriver_path = settings.FIREFOX_DRIVER_PATH
        self.__proxy = settings.PROXIES
        self.__driver = self.__initialize_driver()

    def __enter__(self):
        return self.__driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__driver.close()
        self.__driver.quit()

    def get_driver(self):
        return self.__driver

    def __initialize_driver(self) -> webdriver:

        useragent = UserAgent()



        firefox_capibilities = webdriver.DesiredCapabilities.FIREFOX
        firefox_capibilities['marionette'] = True

        # wd_proxy = self.__proxy['http']
        # firefox_capibilities['proxy'] = {
        #    'proxyType': 'MANUAL',
        #    'httpProxy': wd_proxy,
        #    'sslProxy': wd_proxy,
        # }

        options = Options()
        options.binary_location = '/opt/firefox/firefox'
        options.set_preference("dom.webnotifications.enabled", False)
        options.set_preference("dom.disable_open_during_load", True)
        options.set_preference("media.autoplay.enabled", False)
        options.set_preference("privacy.trackingprotection.enabled", True)
        options.set_preference("general.useragent.override", useragent.random)
        options.add_argument("--headless")
        options.add_argument("--private")

        service = Service(executable_path=self.__geckodriver_path)
        driver: webdriver = webdriver.Firefox(
            service=service,
            options=options,
        )

        timeout = 100
        driver.set_page_load_timeout(timeout)

        return driver
