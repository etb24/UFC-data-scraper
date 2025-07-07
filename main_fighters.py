from fighter_scraper.scraper import get_fighter_urls
from fighter_scraper.parser import parse_fighter_data
from fighter_scraper.writer import write_to_csv
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def main(pages=3):
    fighter_urls = get_fighter_urls(pages)
    print(f"Collected {len(fighter_urls)} fighter URLs.")
    fighter_data_list = []

    for url in tqdm(fighter_urls, desc="Scraping fighter data"):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive'
            }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        fighter_data = parse_fighter_data(soup)
        fighter_data_list.append(fighter_data)

    write_to_csv(fighter_data_list)


if __name__ == "__main__":
    main(pages=2)
