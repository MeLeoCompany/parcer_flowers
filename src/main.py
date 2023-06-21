import requests
from bs4 import BeautifulSoup

def main():
    storage_number = 1
    page_form = "?page="
    link_form = "https://www.florist.ru/"
    block_name = '_3Eluqiay'
    link = link_form + page_form + str(storage_number)
    response = requests.get(link)
    page_text = response.text
    soup = BeautifulSoup(page_text, "html")
    blocks = soup.find_all('div', class_ = block_name)
    # images_link = list(map(lambda block: block.img['src'], blocks))



if __name__ == "__main__":
    main()