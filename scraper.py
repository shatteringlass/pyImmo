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

    ADS_NO = 0
    MAX_ADS = 10000

    def get_pages(self):
        i = 1
        while i:
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
            logging.debug(f"Now scraping page {page_url}")
            urls = self.get_urls_from_page(page_url)
            self.ADS_NO += len(urls)
            yield urls
            if self.ADS_NO >= self.MAX_ADS:
                logging.debug("URL collection completed, exiting.")
                break
            logging.debug("Page completed, now sleeping for 1sec")
            time.sleep(1)

    def get_ad(self, id):
        page = f"https://www.immobiliare.it/annunci/{id}/"
        soup = BeautifulSoup(self.base_request(page).text, 'lxml')
        title = soup.find('h1', {'class': 'title-detail'}).text.strip()
        
        if 'asta' in title.lower() or title.lower().startswith('villa'):
            return None
        
        desc = None
        size = None
        level = 0
        brooms = None
        rooms = None

        p = soup.find('li', {'class': 'features__price'}).text.strip()
        try:
            price = int(''.join(re.findall(r'(\d+)', p)))
        except ValueError:
            price = -1  # Prezzo su richiesta

        features = soup.find('ul', {'class': 'features__list'}).find_all('li')

        for f in features:
            if 'locali' in f.text:
                rooms = f.find('span').text.strip()
            elif 'bagni' in f.text:
                brooms = f.find('span').text.strip()
            elif 'piano' in f.text:
                level = f.find('abbr').text.strip()
            elif 'superficie' in f.text:
                size = f.find('span').text.strip()

        if not(size):
            size = int(float(soup.select(
                'div.row.overflow-x-auto.box-consistenze table tfoot tr td div')[0].text.replace(',', '.')))

        try:
            desc = soup.find('div', {'class': 'description-text'}).text.strip()
        except AttributeError:
            pass

        ha = HouseAdvert(adid=id, title=title, description=desc, price=price,
                         rooms=rooms, size=size, bathrooms=brooms, level=level)
        logging.debug(ha)
        return ha
