import importlib.resources as pkg_resources
import re
from abc import ABCMeta, abstractmethod
from io import SEEK_SET, BytesIO

from PIL import Image, ImageDraw, ImageFont

from .canvas import GreyCanvas, RGBCanvas
from .charwidth import string_width
from .config import ColorTextDrawerConfig, Config
from .typesetting import IgnorableTypeSetting, TypeSetting

__all__ = ("SimpleTextDrawer", "ColorTextDrawer")


class TextDrawer(metaclass=ABCMeta):
    conf: Config
    # conf 的修改要动态地反馈到 ts 上
    ts: TypeSetting
    fontsize: int = 14

    _font_binary: BytesIO = None
    _font: ImageFont.ImageFont = None
    _last_fontpath: str | None = None
    _last_fontsize: int | None = None

    def __init__(self) -> None:
        self.conf = Config()
        self.ts = TypeSetting(self)
        pass

    @property
    def font(self) -> ImageFont.FreeTypeFont:
        """加载字体，如果路径为 package:/// 开头则加载包里的字体文件。
        如果路径或字号变动了，就重新加载字体。
        """
        if self._font is None:
            # 未初始化
            self._read_font(self.conf.font.path)
            self._last_fontpath = self.conf.font.path
            self._load_font(self.fontsize)
            self._last_fontsize = self.fontsize
            return self._font
        # 如果字体路径变动了，重新读取并加载
        if self._last_fontpath != self.conf.font.path:
            self._read_font(self.conf.font.path)
            self._last_fontpath = self.conf.font.path
            self._load_font(self.fontsize)
            self._last_fontsize = self.fontsize
            return self._font
        # 如果字号变动了，重新加载
        if self._last_fontsize != self.fontsize:
            self._load_font(self.fontsize)
            self._last_fontsize = self.fontsize
            return self._font

        return self._font

    def _read_font(self, path: str):
        "读取字体内容到字节缓冲区"
        if path.startswith("package:///"):
            path = path[11:]
            with pkg_resources.files(__package__).joinpath(path).open("rb") as fc:
                self._font_binary = BytesIO(fc.read())
        else:
            with open(path, "rb") as fc:
                self._font_binary = BytesIO(fc.read())
        self._font_binary.seek(0, SEEK_SET)

    def _load_font(self, fontsize: int):
        "从字节缓冲区内读取对应字号的字体"
        self._font_binary.seek(0, SEEK_SET)
        self._font = ImageFont.truetype(self._font_binary, size=fontsize)
        self._font_binary.seek(0, SEEK_SET)

    def text_size(self, text: list[str] | str):
        "计算文本区的宽、高，单位是字"
        if isinstance(text, str):
            return self._text_size_str(text)
        elif isinstance(text, list):
            return self._text_size_list(text)
        else:
            raise TypeError(f"need list[str] or str, but got {type(text)!r}", text)

    def _text_size_list(self, lines: list[str]) -> tuple[int, int]:
        """计算折行完成后的文本区尺寸 (宽, 高)"""
        height = len(lines)
        width = max(string_width(line) for line in lines)
        return (width, height)

    def _text_size_str(self, text: str) -> tuple[int, int]:
        """计算折行前的文本区尺寸 (宽, 高)"""
        lines = self.ts.wrap_text(text)
        return self._text_size_list(lines)

    def fontbox_size(self) -> tuple[int, int]:
        """根据字体设置计算字体盒尺寸 (宽, 高)，单位 px"""
        # EN sign，对应一格宽度
        _, _, fw, fh = self.font.getbbox("\u2002")
        return (fw, fh)

    def canvas_size(self, textsize: tuple[int, int]) -> tuple[int, int]:
        """根据文本尺寸、字体设置、布局设置计算画布尺寸 (宽, 高)，单位 px"""
        tw, th = textsize
        um, rm, dm, lm = self.conf.layout.margin
        up, rp, dp, lp = self.conf.layout.padding
        sp = self.conf.layout.spacing
        fw, fh = self.fontbox_size()
        width = lm + lp + tw * fw + rm + rp
        height = um + up + th * fh + sp * (th - 1) + dm + dp

        return (width, height)

    def text_position(self) -> tuple[int, int]:
        """根据字体设置、布局设置计算文本渲染起点位置 (宽, 高)，单位 px"""
        um, _, _, lm = self.conf.layout.margin
        up, _, _, lp = self.conf.layout.padding
        w = lm + lp
        h = um + up

        return (w, h)

    @abstractmethod
    def draw(self, text: str) -> Image.Image:
        """将 text 文本绘制到图片上，自动生成合适的画布"""
        raise NotImplementedError


class SimpleTextDrawer(TextDrawer):
    """简单的文本绘制工具，自动生成一个刚好包括住被折行文本的图像，渲染文本。
    生成的图像是无透明通道的灰度图，不支持彩色。

    可以自定义的配置属性有：

    + `self.fontsize` : 字号，默认14
    + `self.fg_color` : 字体颜色，默认白色 0xff
    + `self.bg_color` : 背景颜色，默认黑色 0x00
    + `self.ts.line_width` : 折行宽度，单位是字，默认 48
    + `self.ts.indentation` : 折行缩进符号，字符串，默认两个空格
    + `self.conf.font.path` : 重新指定一个字体，需要输入 TTF 格式的字体路径
    + `self.conf.layout.margin` : 上右下左顺序的四元组，单位 px，默认全 6px
    + `self.conf.layout.padding` : 上右下左顺序的四元组，单位 px，默认全 2px
    + `self.conf.layout.spacing` : 行距，单位 px，默认 2px

    ```py
    from impaper import SimpleTextDrawer


    std = SimpleTextDrawer()
    std.ts.indentation = ">>>"
    im = std.draw(
        "abcdefg,abcdefg,abcdefg\n"
        "你好世界，你好世界，你好世界。\n"
        "你好世界，你好世界，你好世界，你好世界，你好世界，你好世界，你好世界，你好世界，你好世界，你好世界，你好世界，你好世界，你好世界，"
    )
    ```
    """

    def __init__(self) -> None:
        super().__init__()
        self.fg_color = 0xFF
        self.bg_color = 0x24

    def draw(self, text: str) -> Image.Image:
        # 准备画布
        lines = self.ts.wrap_text(text)
        text_size = self._text_size_list(lines)
        canvas_size = self.canvas_size(text_size)
        canvas_builder = GreyCanvas()
        canvas_builder.size(canvas_size)
        canvas_builder.background(self.bg_color)
        canvas = canvas_builder.build()
        drawboard = ImageDraw.Draw(canvas)

        # 寻找作画区域
        left, up = self.text_position()
        _, fh = self.fontbox_size()
        # 绘制文字
        for i, line in enumerate(lines):
            x = left
            y = up + fh * i + i * self.conf.layout.spacing
            drawboard.text(
                xy=(x, y),
                text=line,
                fill=self.fg_color,
                font=self.font,
            )

        return canvas


class ColorTextDrawer(TextDrawer):
    """简单的文本绘制工具，自动生成一个刚好包括住被折行文本的图像，渲染文本。
    可通过 <style><style/>标签来标注某段文本，以生成对应颜色的文字图像。

    可以自定义的配置属性有：

    + `self.fontsize` : 字号，默认14
    + `self.fg_color` : 字体颜色，默认白色 0xff
    + `self.bg_color` : 背景颜色，默认黑色 0x00
    + `self.ts.line_width` : 折行宽度，单位是字，默认 48
    + `self.ts.indentation` : 折行缩进符号，字符串，默认两个空格
    + `self.conf.font.path` : 重新指定一个字体，需要输入 TTF 格式的字体路径
    + `self.conf.layout.margin` : 上右下左顺序的四元组，单位 px，默认全 6px
    + `self.conf.layout.padding` : 上右下左顺序的四元组，单位 px，默认全 2px
    + `self.conf.layout.spacing` : 行距，单位 px，默认 2px
    + `self.conf.colors` : 为一个字典，存储了 标签名 => HEX 格式的颜色

    在文本中可以使用类似 HTML 的标签 <Color>text<Reset/> 来标记一段文本的颜色。
    和 HTML 不同的是，只支持一种闭合标签 -- <Reset/>，作用是将颜色重设为默认
    (即self.fg_color)。

    ```py
    from impaper import ColorTextDrawer


    ctd = ColorTextDrawer()
    ctd.fg_color = ctd.conf.colors["Peach"]
    im = ctd.draw(
        "abcdefg,abcdefg,abcdefg\n"
        "你好世界，你好世界，<Yellow>你好世界。<Reset/>\n"
        "你好世界，你好世界，你好世界，你好世界，<Red>你好世界<Reset/>，你好世界，你好世界，你好世界，你好世界，你好世界，你好世界，你好世界，你好世界，"
    )
    ```
    """

    def __init__(self) -> None:
        self.__conf = ColorTextDrawerConfig()
        self._labels = set(f"<{i}>" for i in self.__conf.colors.keys())
        self._labels.add("<Reset/>")
        self._labels_re = re.compile("|".join(self._labels))
        self.ts = IgnorableTypeSetting(caller=self, labels=self._labels)
        self.fg_color = self.conf.colors["Text"]
        self.bg_color = self.conf.colors["Crust"]

    @property
    def conf(self):
        return self.__conf

    @conf.setter
    def conf(self, conf: ColorTextDrawerConfig):
        merged = self.__conf.dict()
        newone = conf.dict()
        merged.update(newone)
        self.__conf = ColorTextDrawerConfig(**merged)
        self._labels = set(f"<{i}>" for i in self.__conf.colors.keys())
        self._labels.add("<Reset/>")
        self._labels_re = re.compile("|".join(self._labels))
        self.ts = IgnorableTypeSetting(
            caller=self, labels=self._labels
        )

    def draw(self, text: str) -> Image.Image:
        # 准备画布
        lines = self.ts.wrap_text(text)
        # 忽略标签计算尺寸
        text_size = self._text_size_list([self._labels_re.sub("", i) for i in lines])
        canvas_size = self.canvas_size(text_size)
        canvas_builder = RGBCanvas()
        canvas_builder.size(canvas_size)
        canvas_builder.background(self.bg_color)
        canvas = canvas_builder.build()
        drawboard = ImageDraw.Draw(canvas)

        # 寻找作画区域
        left, up = self.text_position()
        fw, fh = self.fontbox_size()
        # 绘制文字
        color = self.fg_color
        for i, line in enumerate(lines):
            x = left
            y = up + fh * i + i * self.conf.layout.spacing
            for ii, token in self.ts.iter_tokens(line):
                if token in self._labels:
                    if token == "<Reset/>":
                        color = self.fg_color
                    else:
                        color_name = token[1:-1]
                        color = self.conf.colors[color_name]
                else:
                    drawboard.text(
                        xy=(x, y),
                        text=token,
                        fill=color,
                        font=self.font,
                    )
                    x += string_width(token) * fw
        return canvas
