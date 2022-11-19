from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pytest
import requests

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
    @pytest.mark.skip
    def test_A_B(self, driver):
        driver.get(main_page)
        driver.find_element(by='css selector', value='[href="/abtest"]').click()

    @pytest.mark.skip
    def test_add_remove_elements(self, driver):
        def list_of_elems():
            return driver.find_elements(by='class name', value='added-manually')
        how_much = 5
        driver.get(main_page)
        driver.find_element(by='css selector', value='[href="/add_remove_elements/"]').click()
        adder = driver.find_element(by='css selector', value='.example>:nth-child(1)')
        [adder.click() for _ in range(how_much)]
        elems = list_of_elems()
        assert len(elems) == how_much, "Invalid number of items created."
        [el.click() for el in elems]
        elems = list_of_elems()
        assert len(elems) == 0, "Not all items have been removed."

    @pytest.mark.skip
    def test_basic_auth(self, driver):
        driver.get(main_page)
        driver.find_element(by='css selector', value='[href="/basic_auth"]').click()
        # There are no hooks in the HTML code that will allow to get to the active window. Also, when logging in,
        # the window does not close. In this case, you need to contact the front-end developers (who don't exist).
        driver.switch_to.active_element.send_keys('user', Keys.TAB, 'admin', Keys.TAB, Keys.TAB, Keys.ENTER)

    @pytest.mark.skip
    def test_broken_images(self, driver):
        driver.get(main_page)
        driver.find_element(by='css selector', value='[href="/broken_images"]').click()
        images = driver.find_elements(by='css selector', value='#content>div>img')
        for image in images:
            link = image.get_attribute('src')
            assert requests.get(link).status_code == 200, 'The web page with the image is not available.'

    def challenging_dom(self, driver):
        driver.get(main_page)

