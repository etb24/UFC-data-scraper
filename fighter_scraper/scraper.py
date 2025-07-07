import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from tqdm import tqdm

BASE_URL = 'https://ufc.com'


def get_fighter_urls(pages=253):
    first_url = 'https://www.ufc.com/athletes/all?gender=All&search=&page='
    urls = [first_url + str(page) for page in range(pages)]

    
    fighter_urls = []
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive'
    }
    for url in tqdm(urls, desc="Fetching fighter URLs"):
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        hrefs = soup.find_all('a', class_='e-button--black')
        for href in hrefs:
            if isinstance(href, Tag) and href.has_attr('href'):
                second_link = href['href']
                fighter_url = BASE_URL + str(second_link)
                fighter_urls.append(fighter_url)

    return fighter_urls