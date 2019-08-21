import logging
import re
import requests
import time

from advert import HouseAdvert
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)


class AdBuilder:

    @staticmethod
    def build(entry):
        pass


class Scraper:

    def __init__(self, session=None, retry_count=1, retry_delay=0, proxies=None):
        self.session = session or requests.Session()
        self.proxies = proxies
        self.retry_count = retry_count
        self.retry_delay = retry_delay

    def base_request(self, url):
        response = self.session.get(url=url, proxies=self.proxies)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise e
        else:
            return response


class ImmoScraper(Scraper):

    MAX_ADS = 10000

    def get_pages(self, start=1):
        if not(isinstance(start, int)) or not(isinstance(end, int)):
            raise Exception
        i = start
        yield f"https://www.immobiliare.it/vendita-case/roma/?criterio=rilevanza&pag={i}"
        i += 1

    def get_urls_from_page(self, page):
        urls = list()
        for li in BeautifulSoup(self.base_request(page).text, 'lxml').find_all('p', {'class': 'titolo'}):
            a = li.find('a')
            if a:
                url = li.find('a').get('href')
            if 'immobiliare.it' in url:
                urls.append((re.search(r'/(\d+)/', url).group(1),))
        return urls


    def get_all_urls(self):
        for page_url in self.get_pages():
            logging.debug(f"{'#'*20}\nNow scraping page {page_url}\n{'#'*20}")
            urls = self.get_urls_from_page(page_url)
            logging.debug(f"Found {len(urls)} urls:\n{urls}")
            yield urls
            logging.debug("Page completed, now sleeping for 1sec")
            time.sleep(1)


    def get_ad(id):
        page = f"https://www.immobiliare.it/annunci/{id}/"
        soup = BeautifulSoup(self.base_request(page).text, 'lxml')
        price = soup.find('li', {'class': 'features__price'}).text
