from bs4 import BeautifulSoup
import requests
import os
from .consts import FILE_PASS, FILE_PASS_PIC, PAGE_NUMBER_NAME

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