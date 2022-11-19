from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time

main_page = 'http://the-internet.herokuapp.com/'


@pytest.fixture(scope='function')
def driver():
    print("\nstart browser for test..")
    driver = webdriver.Chrome()
    yield driver
    print("\nquit browser..")
    driver.quit()


class TestMainPage:
    def test_A_B(self, driver):
        driver.get(main_page)
        driver.find_element(by='css selector', value='[href="/abtest"]').click()

    @pytest.mark.skip
    def test_add_remove_elements(self, driver):
        driver.get(main_page)
        driver.find_element(by='css selector', value='.kitt-header-sections__dropdown')

    @pytest.mark.skip
    def test_about_the_bank(self, driver):
        driver.get(main_page)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "li.kitt-top-menu__item_first:nth-child(1) > a:nth-child(2)"))).click()

