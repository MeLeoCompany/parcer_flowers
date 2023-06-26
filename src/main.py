import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

DRIVER_PASS = "C:\\Projects_Learn\\Parce_Flowers\\chromedriver\\chromedriver.exe"
PAGE_FORM = "?page="
LINK_FORM = "https://www.florist.ru/"
BLOCK_NAME = '_3Eluqiay'
BLOCK_NAME_SCROLE = '_3fIsQ45s'
PAGE_NUMBER_NAME = 'CaZoSunN'
TITLE_NAME = '_3JY3BA25 _2LImwTb0'
FILE_PASS = "C:\\Projects_Learn\\Parce_Flowers\\Dataset"
FILE_PASS_PIC = "C:\\Projects_Learn\\Parce_Flowers\\DatasetPic"

def find_max_pages(driver, link):
    driver.get(url = link)
    page_text = driver.page_source 
    soup = BeautifulSoup(page_text, "html.parser")
    page_number_blocks = soup.find_all('div', class_ = PAGE_NUMBER_NAME)
    page_numbers_list = list(map(lambda block: int(block.text) if str.isnumeric(block.text) else 0, page_number_blocks))
    page_number = max(page_numbers_list) + 1
    return page_number

def create_directory(source):
    for name, link in source.items():
        name = name.replace('"', '')
        name = name.replace(':', '')
        os.mkdir(FILE_PASS+"\\"+name)
        p = requests.get(link)
        out = open(FILE_PASS+"\\"+name+'\\img.jpg', "wb")
        out.write(p.content)
        out.close() 

def collect_pic(source):
    i = 1
    for link in source.values():
        p = requests.get(link)
        out = open(FILE_PASS_PIC+f'\\img{i}.jpg', "wb")
        out.write(p.content)
        out.close()
        i += 1

def main():
    source = dict()
    titles = []
    source_urls = []
    base_number = 1
    link = LINK_FORM + PAGE_FORM + str(base_number)
    service = Service(executable_path=DRIVER_PASS)
    driver = webdriver.Chrome(service=service)
    try:
        page_number = find_max_pages(driver, link)
        for number in range(1, 5):
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
        collect_pic(source)
        # create_directory(source)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit



if __name__ == "__main__":
    main()