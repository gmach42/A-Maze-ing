from abc import ABC, abstractmethod

from src.core import ImgData


class Image(ABC):
    @abstractmethod
    def draw(self, img_data: ImgData) -> None:
        pass



