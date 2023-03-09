import requests, requests.adapters
import file_utils
import os


class WebScraperCore():
    # Constants
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0'
    HEADERS = {'User-Agent': USER_AGENT}
    MAX_RETRIES = 10
    BACKOFF_FACTOR = 10
    STATUS_FORCELIST = [ 500, 502, 503, 504 ]


    def __init__(self) -> None:
        # Set up session
        retries = requests.adapters.Retry(
            total=self.MAX_RETRIES, 
            backoff_factor=self.BACKOFF_FACTOR, 
            status_forcelist=self.STATUS_FORCELIST)
        self.session = requests.Session()
        self.session.mount('https://', requests.adapters.HTTPAdapter(max_retries=retries))

        # Set default property values
        self.downloads_root_dir = file_utils.USER_DOWNLOADS_DIR 
        self.app_name = ''

 
    def get_html_webpage_content(self, url: str) -> bytes:
        with self.session.get(url, headers=self.HEADERS) as response:
            # Raise HTTPError, if one occured
            response.raise_for_status()
            return response.content
        

    def download_file(self, url: str, filename: str, replace_existing: bool = False) -> None:
        filename = file_utils.sanitize_filename(filename)
        if filename == '':
            raise ValueError('Filename argument can not be an empty string!')
        dirpath = os.path.join(self.downloads_root_dir, self.app_name)
        
        if not replace_existing:
            filename = file_utils.resolve_duplicate_filenames(dirpath, filename)

        with self.session.get(url, headers=self.HEADERS) as response:
            # Raise HTTPError, if one occured
            response.raise_for_status()

            file_utils.create_dirpath(dirpath)
            filepath = os.path.join(dirpath, filename)

            with open(filepath, 'wb') as file:
                file.write(response.content)
