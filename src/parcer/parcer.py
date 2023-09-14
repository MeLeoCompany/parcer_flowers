import base64
import re
import time
import logging
import json
from dataclasses import dataclass, asdict
from typing import List, Optional

from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from .classificator import varify_pics
from .services import choose_driver, download_pics
from .consts import (BLOCK_NAME, BLOCK_NAME_SCROLE,
                     LINK_FORM, PAGE_FORM, TITLE_NAME, 
                     PAGE_NUMBER_NAME, PAGE_PRODUCT_NAME)

@dataclass
class DataStracture():
    
    source_image_url: Optional[str] = None 
    product_page_url: Optional[str] = None
    title: Optional[str] = None
    article: Optional[str] = None
    pic_code: Optional[str] = None

    def verify_data(self) -> bool:
        confirm = True
        if self.pic_code == b'':
            confirm = False
            logging.warning(f'Блок с артиклом {self.article} удален по причине отсутствия фотографии')
            return confirm
        attributes = self.__annotations__.keys()
        all_attributes_not_none = all(getattr(self, attr) is not None for attr in attributes)
        if all_attributes_not_none is False:
            logging.warning(f'Блок с артиклом {self.article} удален по причине недостатка данных')
            confirm = False
            return confirm
        is_flowers_on_picture = varify_pics(self.pic_code)
        if is_flowers_on_picture is False:
            logging.warning(f'На изображении с артиклом {self.article} изображены не цветы, '
                         'поэтому они удалены')
            confirm = False
            return confirm
        else:
            logging.info(f'Изображение с артиклом {self.article} добавлено')
        return confirm

class Parcer():

    base_link: str = LINK_FORM + PAGE_FORM

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Parcer, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.driver = choose_driver()
        self.link: str = LINK_FORM + PAGE_FORM
        self.collect_data: List[DataStracture]= []
        self.page_number: int = 1

    def link_encriment(self):
        self.page_number += 1 
        self.link = self.base_link + str(self.page_number)

    def find_max_pages(self):
        if hasattr(self, 'max_page_number'):
            logging.warning(f"Максимальное число уже найдено: {self.max_page_number}")
            return None
        self.get_page()
        page_text = self.driver.page_source 
        soup = BeautifulSoup(page_text, "html.parser")
        page_number_blocks = soup.find_all('div', class_ = PAGE_NUMBER_NAME)
        page_numbers_list = list(map(
            lambda block: int(block.text) if str.isnumeric(block.text) else 0, page_number_blocks)
        )
        self.max_page_number = max(page_numbers_list) + 1
        return self.max_page_number

    def get_page(self):
        try:
        # Загрузите веб-страницу
            self.driver.get(url=self.link)
        except WebDriverException as e:
        # Обработка ошибок, которые могли возникнуть при загрузке страницы
            logging.error(f"Произошла ошибка при загрузке страницы: {e}")
    
    def run(self, collection):
        self.find_max_pages()
        while self.page_number < self.max_page_number:
            self.get_page()
            search_boxes = self.driver.find_elements(By.CLASS_NAME, BLOCK_NAME_SCROLE)
            actions = ActionChains(self.driver)
            for search_box in search_boxes:
                actions.move_to_element(search_box).perform()
                time.sleep(0.01)
            page_text = self.driver.page_source
            soup = BeautifulSoup(page_text, "html.parser")
            blocks = soup.find_all('div', class_ = BLOCK_NAME_SCROLE)
            for block in blocks:
                if block.find('div', class_ = BLOCK_NAME) is None:
                    continue
                collect_block = DataStracture()
                collect_block.title = block.find('span', class_ = TITLE_NAME).text
                collect_block.source_image_url = block.find('div', class_ = BLOCK_NAME).img['src']
                page_product_url = block.find('a', class_ = PAGE_PRODUCT_NAME).get('href')
                collect_block.product_page_url = page_product_url
                collect_block.article = re.search(r'\b(\d+)\b', page_product_url).group(1)
                collect_block.pic_code = download_pics(collect_block.source_image_url)
                confirm = collect_block.verify_data()
                if confirm:
                    collect_block.pic_code = base64.b64encode(collect_block.pic_code).decode('utf-8')
                    self.collect_data.append(collect_block)
                else:
                    continue
            if self.collect_data:
                dict_list = [asdict(block) for block in self.collect_data]
                collection.insert_many(dict_list)
                logging.info(f'Данные со страницы {self.page_number} собраны и добавлены в базу данных')
                self.collect_data = []
            else:
                logging.info(f'Нужных данных на странице {self.page_number} не оказалось')
            self.link_encriment()
        self.close()

    def close(self):
        self.driver.close()
        self.driver.quit
