from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import pytest
import requests
import pyautogui
import os
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

    @pytest.mark.skip
    def test_challenging_dom(self, driver):
        driver.get(main_page)
        driver.find_element(by='css selector', value='[href="/challenging_dom"]').click()
        driver.find_element(by='css selector', value='.large-2>:nth-child(1)').click()
        driver.find_element(by='css selector', value='.large-2>:nth-child(3)').click()
        driver.find_element(by='css selector', value='.large-2>:nth-child(5)').click()

    @pytest.mark.skip
    def test_checkboxes(self, driver):
        driver.get(main_page)
        driver.find_element(by='css selector', value='[href="/checkboxes"]').click()
        driver.find_element(by='css selector', value='#checkboxes>:nth-child(1)').click()
        driver.find_element(by='css selector', value='#checkboxes>:nth-child(3)').click()

    @pytest.mark.skip
    def test_context_menu(self, driver):
        driver.get(main_page)
        driver.find_element(by='css selector', value='[href="/context_menu"]').click()
        hot_spot = driver.find_element(by='id', value='hot-spot')
        action = ActionChains(driver)
        action.move_to_element(hot_spot)
        action.context_click(hot_spot).perform()
        alert = driver.switch_to.alert
        assert alert.text == 'You selected a context menu', "Right-clicking on a selection didn't work."

    @pytest.mark.skip
    def test_dissapearing_button(self, driver):
        def try_to_find_an_element():
            return driver.find_element(by='css selector', value='[href="/gallery/"]')
        driver.get(main_page)
        driver.find_element(by='css selector', value='[href="/disappearing_elements"]').click()
        for _ in range(20):
            try_to_find_an_element().click()
            driver.back()
            driver.refresh()

    @pytest.mark.skip
    def test_drag_and_drop(self, driver):
        driver.get(main_page)
        driver.find_element(by='css selector', value='[href="/drag_and_drop"]').click()
        driver.set_script_timeout(30)
        with open('for_drag_and_drop.js', 'r') as src:
            row = src.readline()
            script = ''
            while row:
                script += row
                row = src.readline()
        driver.execute_script(script + "$('#column-a').simulateDragDrop({ dropTarget: '#column-b'});")
        assert driver.find_element(by='css selector', value='#column-a>header').text == 'B', "Blocks are not swapped."

    @pytest.mark.skip
    def test_dropdown(self, driver):
        driver.get(main_page)
        driver.find_element(by='css selector', value='[href="/dropdown"]').click()
        lst = Select(driver.find_element(by='id', value='dropdown'))
        lst.select_by_value('1')

    @pytest.mark.skip
    def test_dynamic_content(self, driver):
        def rows():
            return driver.find_elements(by='css selector', value='div.large-10:nth-child(1) > .row > .large-10')
        driver.get(main_page)
        driver.find_element(by='css selector', value='[href="/dynamic_content"]').click()
        texts1 = [row.text for row in rows()]
        driver.refresh()
        texts2 = [row.text for row in rows()]
        assert texts1 == texts2, 'Refreshing the page changes the content.'

    @pytest.mark.skip
    def test_dynamic_controls(self, driver):
        driver.get(main_page)
        driver.find_element(by='css selector', value='[href = "/dynamic_controls"]').click()
        driver.find_element(by='css selector', value='#checkbox-example >button').click()
        driver.find_element(by='id', value='checkbox').click()
        driver.find_element(by='id', value='checkbox').click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#checkbox-example >button')))
        try:
            driver.find_element(by='id', value='checkbox').click()
        except NoSuchElementException:
            assert True
        else:
            assert False, "The checkbox should have disappeared from the page."

    @pytest.mark.skip
    def test_entry_ad(self, driver):
        driver.get(main_page)
        driver.find_element(by='css selector', value='[href="/entry_ad"]').click()
        driver.switch_to.active_element.send_keys(Keys.ENTER)

    @pytest.mark.skip
    def test_out_of_the_viewport(self, driver):
        driver.get(main_page)
        driver.find_element(by='css selector', value='[href="/exit_intent"]').click()
        pyautogui.moveTo(1000, 1000, 0.2)
        pyautogui.moveTo(0, 0, 0.2)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.modal-footer > p')))
        driver.switch_to.active_element.find_element(by='css selector', value='.modal-footer > p').click()

    @pytest.mark.skip
    def test_download_files(self, driver):
        driver.get(main_page)
        driver.find_element(by='css selector', value='[href="/download"]').click()
        objects = driver.find_elements(by='css selector', value='.example > :nth-child(2n)')
        if not os.path.exists('downloads'):
            os.mkdir('downloads')
        for obj in objects:
            link = obj.get_property('href')
            name = obj.text
            with open('downloads/' + name, 'wb') as file:
                target = requests.get(link)
                file.write(target.content)
        assert len(os.listdir('downloads')) > 0, "The files didn't download."

    @pytest.mark.skip
    def test_upload_files(self, driver):
        driver.get(main_page)
        driver.find_element(by='css selector', value='[href = "/upload"]').click()
        file_to_upload = os.getcwd() + r'\for_drag_and_drop.js'
        driver.find_element(by='id', value='file-upload').send_keys(file_to_upload)
        driver.find_element(by='id', value='file-submit').click()
        result = driver.find_element(by='css selector', value='.example > h3').text
        assert result == 'File Uploaded!', "The file has not been uploaded to the Internet."

    @pytest.mark.skip
    def test_floating_menu(self, driver):
        driver.get(main_page)
        driver.find_element(by='css selector', value='[href="/floating_menu"]').click()
        driver.execute_script("scroll(0, 250)")
        driver.find_element(by='css selector', value='[href = "#home"]').click()
