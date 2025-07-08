from bs4 import BeautifulSoup
from bs4.element import Tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

BASE_URL = 'https://www.ufc.com'

def create_driver():
    service = Service(executable_path='chromedriver.exe')  # adjust path as necessary
    options = Options()
    options.add_argument("--lang=en-US")

    return webdriver.Chrome(service=service, options=options)

def get_fighter_urls(driver, pages=1):
    fighter_urls = []
    base_url = 'https://www.ufc.com/athletes/all?gender=All&search=&page='

    for page in range(pages):
        driver.get(base_url + str(page))
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        links = soup.find_all('a', class_='e-button--black')

        for link in links:
            if isinstance(link, Tag):
                href = link.get('href')
                if isinstance(href, str) and href.startswith('/athlete/'):
                    full_url = BASE_URL + href
                    if full_url not in fighter_urls:
                        fighter_urls.append(full_url)

    return fighter_urls