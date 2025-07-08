from fighter_scraper.scraper import create_driver, get_fighter_urls
from fighter_scraper.parser import parse_fighter_data
from fighter_scraper.writer import write_to_csv

def main():
    driver = create_driver()

    try:
        driver.get("https://www.ufc.com/")
        driver.add_cookie({'name': 'language', 'value': 'en'})
        urls = get_fighter_urls(driver, pages = 275) #~3000 fighters
        fighters = [parse_fighter_data(driver, url) for url in urls]
        write_to_csv(fighters)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
