import logging
from dataclasses import dataclass, field
from typing import List, Optional
from .classificator import varify_pics

@dataclass
class FlowerInfo():
    description: Optional[str] = None
    amount: Optional[int] = None

@dataclass
class ContentData():
    all_text_data: Optional[str] = ''
    flowers: List[FlowerInfo] = field(default_factory=list)

@dataclass
class DataStracture():
    
    source_image_url: Optional[str] = None 
    product_page_url: Optional[str] = None
    title: Optional[str] = None
    article: Optional[str] = None
    pic_code: Optional[str] = None
    content: ContentData = field(default_factory=ContentData)

    def verify_data(self) -> bool:
        confirm = True
        if self.pic_code == b'':
            confirm = False
            logging.warning(f'Блок с артиклом {self.article} удален по причине отсутствия фотографии')
            return confirm
        attributes = self.__annotations__.keys()
        all_attributes_not_none = all(getattr(self, attr) is not None for attr in attributes)
        if all_attributes_not_none is False:
            logging.warning(f'Блок с артиклом {self.article} удален по причине недостатка данных')
            confirm = False
            return confirm
        is_flowers_on_picture = varify_pics(self.pic_code)
        if is_flowers_on_picture is False:
            logging.warning(f'На изображении с артиклом {self.article} изображены не цветы, '
                         'поэтому они удалены')
            confirm = False
            return confirm
        else:
            logging.info(f'Изображение с артиклом {self.article} добавлено')
        return confirm