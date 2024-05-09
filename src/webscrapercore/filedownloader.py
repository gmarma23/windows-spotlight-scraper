import asyncio
from httpx import AsyncClient, Limits, Timeout, HTTPStatusError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception
import aiofiles
from pathlib import Path
from tqdm import tqdm


from webscrapercore.webfile import WebFile
from webscrapercore.useragent import UserAgent


class FileDownloader():
    def __init__(
        self, 
        max_connections: int = 1, 
        max_keepalive_connections: int = 1, 
        timeout: float = 10.0, 
        connect_timeout: float = 30.0, 
        chunk_size: int = 8192,
        retries: int = 10,
        backoff_factor: float = 1,
        status_forcelist: list[int] = [500, 502, 503, 504],
        user_agent: str = UserAgent.random(), 
        overwrite_duplicates: bool = False,
        show_progress: bool = True
    ):

        self._headers = { 
            'User-Agent': str(user_agent)
        }

        self._limits = Limits(
            max_connections=max_connections,
            max_keepalive_connections=max_keepalive_connections
        )

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

        self._chunk_size = chunk_size
        self._overwrite_duplicates = overwrite_duplicates
        self._show_progress = show_progress


    def download_files(self, web_files: list[WebFile]) -> None:
        if self._show_progress:
            with tqdm(total=len(web_files), desc='Downloaded Files') as pbar:
                asyncio.run(self._download_batch(web_files, pbar))
        else:
            asyncio.run(self._download_batch(web_files, None))


    async def _download_batch(self, web_files: list[WebFile], pbar: tqdm) -> None:
        async with AsyncClient(headers=self._headers, limits=self._limits, timeout=self._timeout) as client:
            async with asyncio.TaskGroup() as task_group:
                tasks = []

                for web_file in web_files:
                    task = task_group.create_task(self._download_single(client, web_file, pbar))
                    tasks.append(task)
                    await asyncio.sleep(0)  

                await asyncio.gather(*tasks)


    async def _download_single(self, client: AsyncClient, web_file: WebFile, pbar: tqdm) -> None:
        @self.retry_policy
        async def _download_single_with_retry():
            async with client.stream('GET', web_file.url) as response:
                response.raise_for_status()

                Path(web_file._parent_dir_path).mkdir(exist_ok=True, parents=True)
                destination = web_file.generate_local_destination(self._overwrite_duplicates)

                async with aiofiles.open(destination, 'wb') as file:
                    async for chunk in response.aiter_bytes(self._chunk_size):
                        await file.write(chunk)

                if pbar:
                    pbar.update(1)
        
        await _download_single_with_retry()