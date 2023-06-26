import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time


PAGE_FORM = "?page="
LINK_FORM = "https://www.florist.ru/"
BLOCK_NAME = '_3Eluqiay'
BLOCK_NAME_SCROLE = '_3fIsQ45s'
PAGE_NUMBER_NAME = 'CaZoSunN'
TITLE_NAME = '_3JY3BA25 _2LImwTb0'

def find_max_pages(driver, link):
    driver.get(url = link)
    page_text = driver.page_source 
    soup = BeautifulSoup(page_text, "html.parser")
    page_number_blocks = soup.find_all('div', class_ = PAGE_NUMBER_NAME)
    page_numbers_list = list(map(lambda block: int(block.text) if str.isnumeric(block.text) else 0, page_number_blocks))
    page_number = max(page_numbers_list) + 1
    return page_number

def main():
    source = dict()
    titles = []
    source_urls = []
    base_number = 1
    link = LINK_FORM + PAGE_FORM + str(base_number)
    service = Service(executable_path='C:\\Projects_Learn\\Parce_Flowers\\chromedriver\\chromedriver.exe')
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
                time.sleep(0.1)
            page_text = driver.page_source
            soup = BeautifulSoup(page_text, "html.parser")
            blocks = soup.find_all('div', class_ = BLOCK_NAME_SCROLE)
            for block in blocks:
                titles.append(block.find('span', class_ = TITLE_NAME).text)
                source_urls.append(block.find('div', class_ = BLOCK_NAME).img['src'])
        source = dict(zip(titles, source_urls))
        print(source)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit

    # images_link = list(map(lambda block: block.img['src'], blocks))



if __name__ == "__main__":
    main()