import time
import random
from selenium import webdriver
from constants import *

def csv_to_dictionary(file_path: str) -> tuple:
    result = None
    count = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not result:
                keys = line.strip().split(';')
                print(keys)
                result = {key: [] for key in keys}
                continue
            
            count += 1
            for i, value in enumerate(line.strip().split(';')):
                result[keys[i]].append(value)
    
    return result, count

class Hand:
    def __init__(self, driver: webdriver.chrome.webdriver.WebDriver):
        self.driver = driver

    def fill_by_id(self, element_id: str, value: str) -> any:
        element = self.driver.find_element(by = webdriver.common.by.By.ID, value = element_id)
        element.clear()
        element.send_keys(value)
        return element

    def fill_by_name(self, element_name: str, value: str) -> any:
        element = self.driver.find_element(by = webdriver.common.by.By.NAME, value = element_name)
        element.clear()
        element.send_keys(value)
        return element

    def fill_by_xpath(self, xpath: str, value: str) -> any:
        element = self.find_by_xpath(xpath)
        element.clear()
        element.send_keys(value)
        return element

    def find_by_xpath(self, xpath: str) -> any:
        return self.driver.find_element(by = webdriver.common.by.By.XPATH, value = xpath)

    def find_by_xpath_at_index(self, xpath: str, index: str) -> any:
        return self.driver.find_elements(by = webdriver.common.by.By.XPATH, value = xpath)[index]

    def fill_by_xpath_at_index(self, xpath: str, value: str, index: int) -> any:
        element = self.find_by_xpath_at_index(xpath, index)
        element.clear()
        time.sleep(1)
        element.send_keys(value)
        return element

    def click_radio(self, keyword: str = "radio_1") -> None: # Leroy-Add
        """Click binary check box, currently not used. It could be used at places like have 'you worked at xxx company' """
        self.driver.find_element(by = webdriver.common.by.By.XPATH, value = '//*[@data-uxi-element-id="' + keyword + '"]').send_keys(webdriver.Keys.SPACE)
        #driver.find_element(by = webdriver.common.by.By.XPATH, value = '//*[@data-uxi-element-id="radio_2"]').send_keys(webdriver.Keys.SPACE)

    def data_selector(self, index: int, year: int, month: int) -> None: # Leroy-Add
        """Given any default year selected in the box, select the year according to the given input by interact with the right and left bottons"""
        
        self.find_by_xpath_at_index('//*[@data-automation-id="dateIcon"]', index).click()
        time.sleep(1)
        
        current_year = int(self.find_by_xpath('//*[@data-automation-id="monthPickerSpinnerLabel"]').text)
        time.sleep(1)
        while current_year > year:
            self.find_by_xpath('//*[@data-automation-id="monthPickerLeftSpinner"]').click()
            current_year -= 1
            time.sleep(1)

        while current_year < year:
            self.find_by_xpath('//*[@data-automation-id="monthPickerRightSpinner"]').click()
            current_year += 1
            time.sleep(1)

        #find_by_xpath(self.driver, '//*[@data-automation-id="monthPickerTileLabel" title="March"]').click()
        self.find_by_xpath_at_index('//*[@data-automation-id="monthPickerTileLabel"]', int(month - 1)).click()
        time.sleep(1)

    def login(self) -> bool:
        element = self.driver.find_element(by = webdriver.common.by.By.XPATH, value = LOGIN_BUTTON_XPATH)
        element.click()

def sleep():
    time.sleep(random.uniform(1.1, 2.1))

def yes_or_not(action_name: str = ""):
    to_proceed = None
    while to_proceed not in ['y', 'n']:
        to_proceed = input(f"{action_name} Proceed? type 'y' or 'n' then enter: ")

    if to_proceed == 'n':
        print("❌ Abort!")
        return False

    print("✅ Proceed!") 
    return True

def enter_and_select(driver: any, value: str):
    pass
