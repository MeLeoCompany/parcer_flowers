import os
import logging
import requests
from dotenv import load_dotenv

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ServiceChrome
from selenium.webdriver.edge.service import Service as ServiceEdge

from .consts import  DRIVER_PASS_CHROME

load_dotenv()

def download_pics(link):
    max_attempts = 5
    success = False
    image_code = None
    for _ in range(max_attempts):
        try:
            response = requests.get(link)
            response.raise_for_status()  # Проверка наличия ошибок HTTP
            image_code = response.content
            if response.status_code == 200:
                success = True
                break
        except requests.exceptions.RequestException as e:
            logging.error(f"Произошла ошибка при запросе изображения: {str(e)}")
        except Exception as e:
            logging.error(f"Произошла неизвестная ошибка: {str(e)}")

    if not success:
        logging.error(f'Не удалось выполнить запрос к {link} после {max_attempts} попыток.')
        raise Exception(f'Не удалось выполнить запрос к {link} после {max_attempts} попыток.')

    return image_code

def init_db_connection():
    client = MongoClient("mongodb://127.0.0.1:27017/")
    db = client.get_database("pics_base")
    # Выберите базу данных
    collection = db['pics_data']
    collection.delete_many({})
    return collection

def choose_driver():

    driver_variable = os.getenv('DRIVER') 

    if driver_variable is None:
        raise KeyError("Ошибка: Переменная DRIVER не установлена в переменных окружения.")   

    if driver_variable == 'Edge':
        service = ServiceEdge()
        driver = webdriver.Edge(service=service)
    elif driver_variable == 'Chrome':
        service = ServiceChrome(executable_path=DRIVER_PASS_CHROME)
        driver = webdriver.Chrome(service=service)
    else:
        raise KeyError("В переменных окружения установлен неопознанный драйвер, " 
                       "пожалуйста используйте 'Edge' или 'Chrome'")

    return driver

def init_logger():
    # Создаем объект логгера
    logger = logging.getLogger()
    # Устанавливаем уровень логирования (например, DEBUG, INFO, WARNING, ERROR, CRITICAL)
    logger.setLevel(logging.DEBUG)
    # Создаем объект для записи логов в файл
    file_handler = logging.FileHandler("my_log.log", mode='w', encoding='utf-8')
    # Устанавливаем уровень логирования для файла
    file_handler.setLevel(logging.DEBUG)
    # Создаем форматтер для логов
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    # Привязываем форматтер к обработчику
    file_handler.setFormatter(formatter)
    # Добавляем обработчик к логгеру
    logger.addHandler(file_handler)
    logging.getLogger('selenium').setLevel(logging.WARNING)
    return logger
