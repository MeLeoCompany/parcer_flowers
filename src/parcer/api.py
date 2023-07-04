from bs4 import BeautifulSoup
import requests
import os
from .consts import FILE_PASS, FILE_PASS_PIC, PAGE_NUMBER_NAME

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