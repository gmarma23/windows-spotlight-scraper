from httpx import Timeout, Client, HTTPStatusError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception

from webscrapercore.useragent import UserAgent


class WebClientPlain():
    def __init__(
        self, 
        timeout: float = 10.0, 
        connect_timeout: float = 30.0, 
        retries: int = 10,
        backoff_factor: float = 1,
        status_forcelist: list[int] = [500, 502, 503, 504],
        user_agent: str = UserAgent.random()
    ):
        super().__init__()

        self._headers = { 
            'User-Agent': user_agent
        }

        self._timeout = Timeout(
            timeout=timeout, 
            connect=connect_timeout
        )

        self.retry_policy = retry(
            stop=stop_after_attempt(retries),
            wait=wait_exponential(multiplier=backoff_factor),
            retry=retry_if_exception(
                lambda e: isinstance(e, HTTPStatusError) and e.response.status_code in status_forcelist
            )
        )

        self._client = Client(headers=self._headers, timeout=self._timeout)


    def get_page_content(self, url: str) -> str:
        @self.retry_policy
        def _get_page_content_with_retry() -> str:
            response = self._client.get(url)
            response.raise_for_status()
            return response.text
        
        return _get_page_content_with_retry()