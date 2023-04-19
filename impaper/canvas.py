from abc import ABCMeta, abstractmethod

from PIL import Image

__all__ = ("GreyCanvas",)

class CanvasBuilder(metaclass=ABCMeta):
    _size: tuple[int, int]

    @abstractmethod
    def size(self, size: tuple[int, int]):
        "设置画布尺寸"
        self._size = size

    @abstractmethod
    def background(self, bg):
        "设置画布背景"
        raise NotImplementedError

    @abstractmethod
    def build(self) -> Image:
        "构建画布图像"
        raise NotImplementedError


class GreyCanvas(CanvasBuilder):
    "灰度画板"

    def __init__(self) -> None:
        super().__init__()
        # 默认黑色背景
        self._color = 0x00
        self._size = (512, 1024)

    def size(self, size: tuple[int, int]):
        return super().size(size)

    def background(self, bg: int):
        "设置画布背景颜色"
        self._color = bg

    def build(self) -> Image:
        canvas = Image.new("L", size=self._size, color=self._color)
        return canvas


class RGBCanvas(CanvasBuilder):
    "支持 RGB 颜色的画板（不含透明通道）"
    def __init__(self) -> None:
        super().__init__()
        # 默认黑色背景
        self._color = (0, 0, 0)
        self._size = (512, 1024)

    def size(self, size: tuple[int, int]):
        return super().size(size)

    def background(self, bg: int):
        "设置画布背景颜色"
        self._color = bg

    def build(self) -> Image:
        canvas = Image.new("RGB", size=self._size, color=self._color)
        return canvas
