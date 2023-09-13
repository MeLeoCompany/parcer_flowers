# Парсинг для магазина florist.ru

При обновлении venv:
pip freeze > requirements.txt

## Установка
1. Создайте виртуальное окружение и установить требуемые библиотеки:
pip install -r requirements.txt
2. Для запуска вам понадобится скачать драйвер для запуска браузера
(обратите внимание на совместимость с текущей версией браузера):
Chrome: https://chromedriver.chromium.org/downloads
или Edge: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
3. В .env укажите драйвер на котором будете парсить 
DRIVER='Edge' или DRIVER='Chrome' 
4. Запустите mondoDB на который будут записываться ваши изображения и другие 
данные:
docker run -d -p 27017:27017 --name mymongodb mongo