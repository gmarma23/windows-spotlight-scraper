import bs4


class HTMLTag():
    def __init__(self, tag: bs4.element.Tag):
        self._tag = tag


    @property
    def text(self) -> str:
        return str(self._tag)


    def get_attributes_list(self) -> list[str]:
        return self._tag.get_attribute_list()

    
    def get_attribute_value(self, attribute: str) -> str:
        return self._tag.get(attribute)
    

    def get_content(self) -> str:
        return self._tag.get_text()
    

    def __str__(self):
        return self.text
    

    def __repr__(self):
        return self.text