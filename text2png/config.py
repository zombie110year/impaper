"""
Config Module, define config object of {ref}`Text2Png`.
"""

from dataclasses import dataclass

@dataclass
class Config:
    # the path of ttf font file
    ttf_font_file: str
