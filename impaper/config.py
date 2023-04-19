"""
Config Module, define config object of {ref}`Text2Png`.
"""

from pydantic import BaseModel, Extra

__all__ = ("Font", "Layout", "Config", "ColorTextDrawerConfig")


class Font(BaseModel, extra=Extra.ignore):
    """
    字体相关设置

    + `path` 字体文件路径，如果为 package:/// 开头则表示从包根目录开始的路径
    + `font` 字体对象
    + `fontsize` 字号，默认 14px
    + `fontcolor` 字体颜色，默认白色
    """

    path: str = "package:///res/sarasa-mono-sc-regular.ttf"


class Layout(BaseModel, extra=Extra.ignore):
    """设置页面布局相关内容

    + `margin`: 外边距，上右下左顺序的四元组，单位 px，默认全 6px
    + `padding`: 内边距，上右下左顺序的四元组，单位 px，默认全 2px
    + `spacing`: 行距，单位 px，默认 2px
    """

    margin: tuple[int, int, int, int] = (6, 6, 6, 6)
    padding: tuple[int, int, int, int] = (2, 2, 2, 2)
    spacing: int = 2


class TypeSettingConfig(BaseModel, extra=Extra.ignore):
    """设置折行、缩进相关内容

    + `line_width`: 多少字符宽度折行，一般的英文字母宽度为1，汉字为2，以此类推
    + `indentation`: 折行后的缩进符号
    """

    line_width: int = 48
    indentation: str = "  "


class Config(BaseModel, extra=Extra.ignore):
    """构造文本转图像引擎的配置对象

    :param ttf_font_path: 指定字体 TTF 文件，默认读取包内的等距更纱黑体SC
    :return: 配置对象
    :exception OSError: 无法读取字体文件时抛出
    """

    font: Font = Font()
    layout: Layout = Layout()
    typesetting: TypeSettingConfig = TypeSettingConfig()


class ColorTextDrawerConfig(Config, extra=Extra.ignore):
    """构造 ColorTextDrawer 的配置对象

    各颜色都是 HEX 代码。默认颜色参考了 Catppuccin Mocha
    (https://github.com/catppuccin/catppuccin) 主题。
    """
    colors: dict[str, tuple[int, int, int]] = {
        "Rosewater": (245, 224, 220),
        "Flamingo": (242, 205, 205),
        "Pink": (245, 194, 231),
        "Mauve": (203, 166, 247),
        "Red": (243, 139, 168),
        "Maroon": (235, 160, 172),
        "Peach": (250, 179, 135),
        "Yellow": (249, 226, 175),
        "Green": (166, 227, 161),
        "Teal": (148, 226, 213),
        "Sky": (137, 220, 235),
        "Sapphire": (116, 199, 236),
        "Blue": (137, 180, 250),
        "Lavender": (180, 190, 254),
        "Text": (205, 214, 244),
        "Subtext1": (186, 194, 222),
        "Subtext0": (166, 173, 200),
        "Overlay2": (147, 153, 178),
        "Overlay1": (127, 132, 156),
        "Overlay0": (108, 112, 134),
        "Surface2": (88, 91, 112),
        "Surface1": (69, 71, 90),
        "Surface0": (49, 50, 68),
        "Base": (30, 30, 46),
        "Mantle": (24, 24, 37),
        "Crust": (17, 17, 27),
    }
