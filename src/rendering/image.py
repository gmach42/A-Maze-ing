from abc import ABC, abstractmethod
from src.core.xvar import ImgData


class Image(ABC):
    @abstractmethod
    def draw(self, img_data: ImgData) -> None:
        pass



