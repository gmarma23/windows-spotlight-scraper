from pathlib import Path

from webscrapercore import FileDownloader, HTMLParser, WebClientPlain, WebFile


class WindowsSpotlightScraper():
    __APP_NAME = 'Windows Spotlight Scraper'
 
    __BASE_URL = 'https://windows10spotlight.com'
    __COLLECTION_PAGE_URL = __BASE_URL + '/page/{0}'


    def __init__(self) -> None:
        self.__downloads = Path.home() / 'Downloads' / self.app_name

        self.__web_client = WebClientPlain()
        self.__file_downloader = FileDownloader(
            max_connections=50,
            max_keepalive_connections=50,
            overwrite_duplicates=True
        )


    @property
    def app_name(self) -> str:
        return WindowsSpotlightScraper.__APP_NAME


    def download_images(self, count: int = None) -> None:           
        web_files = list(map(self.__image_page_2_web_file, self.__gather_image_page_urls(count)))

        self.__file_downloader.download_files(web_files)


    def __gather_image_page_urls(self, count: int = None) -> list[str]:
        total_collection_pages = self.__get_total_collection_pages_count()

        image_page_urls = self.__get_image_page_urls(WindowsSpotlightScraper.__BASE_URL)
        i = 2

        while i <= total_collection_pages and (not count or len(image_page_urls) < count):
            urls = self.__get_image_page_urls(WindowsSpotlightScraper.__COLLECTION_PAGE_URL.format(i))
            image_page_urls.extend(urls)
            i += 1

        if count:
            image_page_urls = image_page_urls[:count]

        return image_page_urls
                        

    def __get_image_page_urls(self, collection_page_url: str) -> list[str]:
        page = self.__web_client.get_page_content(collection_page_url)
        parser = HTMLParser(page)

        image_page_urls = [item.get_attribute_value('href') for item in parser.get_elements('a', ['anons-thumbnail', 'show'])]

        return image_page_urls
    
    
    def __image_page_2_web_file(self, image_page_url: str) -> WebFile:
        page = self.__web_client.get_page_content(image_page_url)
        parser = HTMLParser(page)

        image_tag = parser.get_elements('img', None, 'a')[0]

        url = image_tag.get_attribute_value('srcset').split(', ')[-1].split(' ')[0] 
        title = image_tag.get_attribute_value('title')
        extension = url.split('.')[-1]
        
        web_file = WebFile(url, title, extension, self.__downloads)

        return web_file
    

    def __get_total_collection_pages_count(self) -> int:
        page = self.__web_client.get_page_content(WindowsSpotlightScraper.__BASE_URL)
        parser = HTMLParser(page)

        count_raw = parser.get_elements('a', 'page-numbers')[-2].get_content()
        count = int(count_raw.replace(',', ''))

        return count