"""
Config Module, define config object of {ref}`Text2Png`.
"""
import importlib.resources as pkg_resources
from dataclasses import dataclass


from PIL import ImageFont


# 手动编写 init 方法
@dataclass(init=False)
class Config:
    """构造文本转图像引擎的配置对象

    :param ttf_font_path: 指定字体 TTF 文件，默认读取包内的等距更纱黑体SC
    :return: 配置对象
    :exception OSError: 无法读取字体文件时抛出
    """

    font: "Font"

    def __init__(self, ttf_font_path: str | None = None) -> None:
        self.font = Font(path=ttf_font_path)


@dataclass
class Font:
    """
    字体相关设置

    + `path` 字体文件路径，如果为 package:/// 开头则表示从包根目录开始的路径
    + `font` 字体对象
    + `fontsize` 字号，默认 14px
    + `fontcolor` 字体颜色，默认白色
    """

    path: str = "package:///res/sarasa-mono-sc-regular.ttf"
    fontsize: int = 14
    fontcolor: int = 0xFF

    _font: ImageFont.ImageFont | None = None
    _last_path: str | None = None
    _last_fontsize: int | None = None

    def __init__(
        self,
        path: str = "package:///res/sarasa-mono-sc-regular.ttf",
        fontsize: int = 14,
        fontcolor: int = 255,
    ) -> None:
        self.path = path
        self.fontsize = fontsize
        self.fontcolor = fontcolor

    @property
    def font(self) -> ImageFont.ImageFont:
        """加载字体，如果路径为 package:/// 开头则加载包里的字体文件。
        如果路径或字号变动了，就重新加载字体。
        """
        if self._font is None:
            self._font = self._load_font(self.path, self.fontsize)
            self._last_path = self.path
            self._last_fontsize = self.fontsize
        if (self._last_fontsize != self.fontsize) or (self._last_path != self.path):
            self._font = self._load_font(self.path, self.fontsize)
            self._last_path = self.path
            self._last_fontsize = self.fontsize
        return self._font

    @staticmethod
    def _load_font(path: str, size: int):
        if path.startswith("package:///"):
            path = path[11:]
            with pkg_resources.files(__package__).joinpath(path).open("rb") as fc:
                imf = ImageFont.truetype(fc, size)
        else:
            imf = ImageFont.truetype(path, size)
        return imf
