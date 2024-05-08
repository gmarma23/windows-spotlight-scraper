from pathlib import Path
import re


class WebFile():
    _ILLEGAL_FILENAME_CHARS = r'[\\/<>:\"|?*\t\n\r]'


    def __init__(self, url: str, name: str, extension: str, parent_dir_path: str):
        self._url = url
        self._name = name
        self._extension = extension
        self._parent_dir_path = Path(parent_dir_path)


    @property
    def url(self) -> str:
        return self._url

    @property
    def name(self) -> str:
        return self._name

    @property
    def extension(self) -> str:
        return self._extension
    
    @property
    def parent_dir_path(self) -> str:
        return self._parent_dir_path.resolve()
    

    def generate_local_destination(self, overwrite_duplicates: bool = False) -> str:      
        filename = self.sanitize_filename()

        if not overwrite_duplicates:
            filename = self._resolve_duplicate_filename(filename)

        destination = self._parent_dir_path / filename
        return destination.resolve()
    

    def sanitize_filename(self) -> str:
        return re.sub(WebFile._ILLEGAL_FILENAME_CHARS, '', f'{self._name}.{self._extension}')


    def _resolve_duplicate_filename(self, filename: str) -> str:
        name, extension = Path(filename).stem, Path(filename).suffix
        i = 1
        
        while (self._parent_dir_path / filename).exists():
            filename = f'{name}({i}){extension}'           
            i += 1

        return filename
    

    def __hash__(self) -> int: 
        return hash(repr(self.__dict__))
    

    def __eq__(self, other) -> bool: 
        if self.__class__ != other.__class__: 
            return False
        
        return self.__dict__ == other.__dict__