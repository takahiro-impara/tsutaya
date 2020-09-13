import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import utils.util


class Chrome:
    driver_path = os.path.abspath(utils.util.resource_path('driver/chromedriver'))
    #driver_path = os.path.abspath('resources/browser-drivers/chromedriver')

    def __init__(self, headless):
        options = Options()
        if headless:
            options.add_argument('--headless')
        self.browser = webdriver.Chrome(self.driver_path, chrome_options=options)

    def close_and_quit(self):
        self.browser.close()
        self.browser.quit()

    def open(self, uri):
        self.browser.get(uri)

    def wait(self, wait_time =10) -> WebDriverWait:
        return WebDriverWait(self.browser, wait_time)

    def find_elements(self, by, value):
        return self.browser.find_elements(by, value)

    def find_element(self, by, value):
        return self.browser.find_element(by, value)

    def switch_to(self):
        return self.browser.switch_to

