import os
import re
import requests
from dotenv import load_dotenv

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ServiceChrome
from selenium.webdriver.edge.service import Service as ServiceEdge

from .consts import  DRIVER_PASS_CHROME

load_dotenv()

def download_pics(link):
    try:
        response = requests.get(link)
        response.raise_for_status()  # Проверка наличия ошибок HTTP
        image_code = response.content
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при запросе изображения: {str(e)}")
    except Exception as e:
        print(f"Произошла неизвестная ошибка: {str(e)}")
    return image_code

def init_db_connection():
    client = MongoClient("mongodb://127.0.0.1:27017/")
    db = client.get_database("pics_base")
    # Выберите базу данных
    collection = db['pics_data']
    return collection

def choose_driver():
    try:
        driver_variable = os.getenv('DRIVER') 
    except KeyError:
        print("Ошибка: Переменная DRIVER не установлена в переменных окружения.")

    if driver_variable == 'Edge':
        service = ServiceEdge()
        driver = webdriver.Edge(service=service)
    elif driver_variable == 'Chrome':
        service = ServiceChrome(executable_path=DRIVER_PASS_CHROME)
        driver = webdriver.Chrome(service=service)
    else:
        raise KeyError("В переменных окружения установлен неопознанный драйвер," 
                       "пожалуйста используйте 'Edge' или 'Chrome'")

    return driver