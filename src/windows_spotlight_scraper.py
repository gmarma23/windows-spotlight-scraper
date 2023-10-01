from webscraper_core import WebScraperCore
from bs4 import BeautifulSoup
from tqdm import tqdm
import file_utils


class WindowsSpotlightScraper():
    APP_NAME = 'Windows Spotlight Scraper'
    BASE_URL = 'https://windows10spotlight.com'
    COLLECTION_PAGE_URL = BASE_URL + '/page/{0}'
    IMAGE_PAGE_URL = BASE_URL + '/images/{0}'
    IMAGES_PER_COLLECTION_PAGE = 5

    def __init__(self) -> None:
        self.webscraper_core = WebScraperCore()
        self.webscraper_core.downloads_root_dir = file_utils.USER_PICTURES_DIR
        self.webscraper_core.app_name = self.APP_NAME


    def download_images(self, remaining_count: int = -1) -> None:
        total_collection_pages = self.get_total_collection_pages_count()
        total_images = self.IMAGES_PER_COLLECTION_PAGE * (total_collection_pages - 1) + \
                              self.get_collection_last_page_images_count()

        if remaining_count <= 0 or remaining_count > total_images:
            remaining_count = total_images
            
        with tqdm(total=remaining_count, desc='Downloading images') as pbar:
            for page_index in range(1, total_collection_pages + 1):
                remaining_count = self.download_page_images(page_index, pbar, remaining_count)
                if remaining_count == 0:
                    return
            

    def download_page_images(self, page_index: int, pbar: tqdm, remaining_count: int = -1) -> int:
        page_url = self.COLLECTION_PAGE_URL.format(page_index)
        html_soup = self.parse_HTML(page_url)
        
        page_links = html_soup.find_all('a', href=True)
        image_page_urls = list(dict.fromkeys([link['href'] for link in page_links if self.is_image_page_url(link['href'])]))

        if remaining_count > 0 and remaining_count < len(image_page_urls):
            image_page_urls = image_page_urls[:remaining_count]

        for url in image_page_urls:
            self.download_image(url)
            pbar.update(1)

        if len(image_page_urls) > 5:
            print(image_page_urls)

        remaining_count -= len(image_page_urls)
        return remaining_count

    
    def download_image(self, image_page_url: str) -> None:
        html_soup = self.parse_HTML(image_page_url)
        img_tag_content = html_soup.find('img') 
        image_url = img_tag_content['srcset'].split(',')[-1].split(' ')[1] 
        image_name = html_soup.find('h1').text
        image_fullname = f'{image_name}.{image_url.split(".")[-1]}'
        self.webscraper_core.download_file(image_url, image_fullname, True)
    

    def get_total_collection_pages_count(self) -> int:
        html_soup = self.parse_HTML(self.COLLECTION_PAGE_URL.format(1))
        count = html_soup.find_all('a', {'class' : 'page-numbers'})[-2].text
        count = count.replace(',', '')
        return int(count)
    

    def get_collection_last_page_images_count(self) -> int:
        last_page_index = self.get_total_collection_pages_count()
        page_url = self.COLLECTION_PAGE_URL.format(last_page_index)
        html_soup = self.parse_HTML(page_url)
        
        page_links = html_soup.find_all('a', href=True)
        image_page_urls = list(dict.fromkeys([link['href'] for link in page_links if self.is_image_page_url(link['href'])]))        
        return len(image_page_urls)


    def is_image_page_url(self, url: str) -> bool:
        return url.startswith(self.IMAGE_PAGE_URL.format('')) and not \
               url.endswith('#respond') and not \
               url.endswith('#comments')


    def parse_HTML(self, url: str) -> BeautifulSoup:
        webpage_content = self.webscraper_core.get_html_webpage_content(url)
        return BeautifulSoup(webpage_content, 'html.parser')
