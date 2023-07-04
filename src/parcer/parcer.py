import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

from .api import collect_pic, find_max_pages
from .consts import BLOCK_NAME, BLOCK_NAME_SCROLE, DRIVER_PASS, LINK_FORM, PAGE_FORM, TITLE_NAME

def parce():
    source = dict()
    titles = []
    source_urls = []
    base_number = 1
    link = LINK_FORM + PAGE_FORM + str(base_number)
    service = Service(executable_path=DRIVER_PASS)
    driver = webdriver.Chrome(service=service)
    try:
        page_number = find_max_pages(driver, link)
        for number in range(1, page_number):
            link = LINK_FORM + PAGE_FORM + str(number)
            driver.get(url = link)
            search_boxes = driver.find_elements(By.CLASS_NAME, BLOCK_NAME_SCROLE)
            actions = ActionChains(driver)
            for search_box in search_boxes:
                actions.move_to_element(search_box).perform()
                time.sleep(0.01)
            time.sleep(1)
            page_text = driver.page_source
            soup = BeautifulSoup(page_text, "html.parser")
            blocks = soup.find_all('div', class_ = BLOCK_NAME_SCROLE)
            for block in blocks:
                if block.find('div', class_ = BLOCK_NAME) is None:
                    continue
                titles.append(block.find('span', class_ = TITLE_NAME).text)
                source_urls.append(block.find('div', class_ = BLOCK_NAME).img['src'])
        # create_directory(source)
    except Exception as ex:
        print(ex)
    finally:
        source = dict(zip(titles, source_urls))
        collect_pic(source)
        driver.close()
        driver.quit