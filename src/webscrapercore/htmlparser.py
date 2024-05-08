from bs4 import BeautifulSoup
from bs4.element import Tag

from webscrapercore.htmltag import HTMLTag


class HTMLParser():
    def __init__(self, content: str):
        self._soup = BeautifulSoup(content, 'html.parser')


    def get_elements_by_tag(self, target_element_tag: str, parent_element_tag: str = None, parent_element_class: str = None) -> list[HTMLTag]:
        parent_elements = self._get_parent_elements(parent_element_tag, parent_element_class)

        target_elements = []
        for parent_element in parent_elements:
            target_elements.extend(list(map(HTMLTag, parent_element.find_all(target_element_tag)))) 

        return target_elements    
    

    def get_elements_by_class(self, target_element_class: str, parent_element_tag: str = None, parent_element_class: str = None) -> list[HTMLTag]:
        parent_elements = self._get_parent_elements(parent_element_tag, parent_element_class)

        target_elements = []
        for parent_element in parent_elements:
            target_elements.extend(list(map(HTMLTag, parent_element.find_all(class_=target_element_class)))) 

        return target_elements
    

    def format_pretty(self) -> str:
        return self._soup.prettify()
    

    def _get_parent_elements(self, parent_element_tag: str, parent_element_class: str) -> list[Tag]:
        if parent_element_tag or parent_element_class:
            return self._soup.find_all(parent_element_tag, class_=parent_element_class)
        else:
            return [self._soup]