import base64
import random
import re
import time
import logging

from dataclasses import asdict
from typing import List

from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

from .data_strutures import ContentData, DataStracture, FlowerInfo

from .services import choose_driver, download_pics
from .consts import (BLOCK_NAME, BLOCK_NAME_SCROLE, BUTTON_SHOW_ALL,
                     LINK_FORM, PAGE_FORM, TITLE_NAME, 
                     PAGE_NUMBER_NAME, PAGE_PRODUCT_NAME,
                     BUKET_DISCRIPTION_NAME, FLOWER_DISCRIPTION,
                     FLOWER_DISCRIPTION_NUMBER)


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
        self.get_page(self.link)
        page_text = self.driver.page_source 
        soup = BeautifulSoup(page_text, "html.parser")
        page_number_blocks = soup.find_all('div', class_ = PAGE_NUMBER_NAME)
        page_numbers_list = list(map(
            lambda block: int(block.text) if str.isnumeric(block.text) else 0, page_number_blocks)
        )
        self.max_page_number = max(page_numbers_list) + 1
        return self.max_page_number

    def get_page(self, url):
        try:
        # Загрузите веб-страницу
            self.driver.get(url)
        except WebDriverException as e:
        # Обработка ошибок, которые могли возникнуть при загрузке страницы
            logging.error(f"Произошла ошибка при загрузке страницы: {e}")

    def find_content_info(self, collect_block):
        self.get_page(collect_block.product_page_url)
        try:
            button = self.driver.find_element(By.CLASS_NAME, BUTTON_SHOW_ALL)
            button.click()
        except NoSuchElementException:
            logging.info(f'Кнопки развернуть все на странице {collect_block.product_page_url} нет')
        page_text = self.driver.page_source
        soup = BeautifulSoup(page_text, "html.parser")
        blocks = soup.find_all('div', class_ = BUKET_DISCRIPTION_NAME)
        for block in blocks:
            description = block.find('span', class_ = FLOWER_DISCRIPTION).text
            if block.find('span', class_ = FLOWER_DISCRIPTION_NUMBER) is None:
                numbers_of_flowers = ''
            else:
                numbers_of_flowers = block.find('span', class_ = FLOWER_DISCRIPTION_NUMBER).text
                numbers_of_flowers = re.search(r'\d+', numbers_of_flowers).group()
                collect_block.content.all_text_data += numbers_of_flowers + ' '
            collect_block.content.all_text_data += description + ';' + ' '
            collect_block.content.flowers.append(FlowerInfo(description, numbers_of_flowers))
        return collect_block


    def run(self, collection):
        self.find_max_pages()
        while self.page_number < self.max_page_number:
            self.get_page(self.link)
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
                collect_block = self.find_content_info(collect_block)
                confirm = collect_block.verify_data()
                time.sleep(random.uniform(0.5, 3.0))
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
