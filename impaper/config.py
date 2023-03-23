"""
Config Module, define config object of {ref}`Text2Png`.
"""

from dataclasses import dataclass, field

__all__ = ("Font", "Layout", "Config")


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


@dataclass
class Layout:
    """设置页面布局相关内容

    + `margin`: 外边距，上右下左顺序的四元组，单位 px，默认全 6px
    + `padding`: 内边距，上右下左顺序的四元组，单位 px，默认全 2px
    + `spacing`: 行距，单位 px，默认 2px
    """

    margin: tuple[int, int, int, int] = (6, 6, 6, 6)
    padding: tuple[int, int, int, int] = (2, 2, 2, 2)
    spacing: int = 2


# 手动编写 init 方法
@dataclass()
class Config:
    """构造文本转图像引擎的配置对象

    :param ttf_font_path: 指定字体 TTF 文件，默认读取包内的等距更纱黑体SC
    :return: 配置对象
    :exception OSError: 无法读取字体文件时抛出
    """

    font: Font = field(default_factory=Font)
    layout: Layout = field(default_factory=Layout)
