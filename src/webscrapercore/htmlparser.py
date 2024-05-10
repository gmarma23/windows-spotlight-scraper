from bs4 import BeautifulSoup
from bs4.element import Tag

from webscrapercore.htmltag import HTMLTag


class HTMLParser():
    def __init__(self, content: str):
        self._soup = BeautifulSoup(content, 'html.parser')
    

    def get_elements(
            self, 
            target_element_tag: str = None, 
            target_element_classes: list[str] = None, 
            parent_element_tag: str = None, 
            parent_element_classes: list[str] = None
        ) -> list[HTMLTag]:
        parent_elements = self._get_parent_elements(parent_element_tag, parent_element_classes)

        target_elements = []

        for parent_element in parent_elements:
            args = (target_element_tag,)

            if target_element_classes:
                args += ({'class': target_element_classes},)

            target_elements.extend(list(map(HTMLTag, parent_element.find_all(*args))))

        return target_elements
    

    def format_pretty(self) -> str:
        return self._soup.prettify()
    

    def _get_parent_elements(self, parent_element_tag: str, parent_element_classes: list[str]) -> list[Tag]:
        if not parent_element_tag and not parent_element_classes:
            return [self._soup]
        
        args = (parent_element_tag,)

        if parent_element_classes:
            args += ({'class': parent_element_classes},)

        return self._soup.find_all(*args)
            