from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
import time

main_page = 'https://www.sberbank.com/index'


class TestMainPage:
    @pytest.fixture(scope='class')
    def driver(self):
        print("\nstart browser for test..")
        driver = webdriver.Chrome()
        yield driver
        print("\nquit browser..")
        driver.quit()

    def test_main_page(self, driver):
        driver.get(main_page)
        time.sleep(5)
        logo = driver.find_element(by='css selector', value='.header__logo-image') #.implicitly_wait(5)
        print(logo.text)


pytest.main()