import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

class Walmart_Selenium:
    def __init__(self, option=None, url="https://www.walmart.com/"):
        self.url = url
        self.option = option
        self.profile = FirefoxProfile()
        self.driver = None