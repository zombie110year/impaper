import exrex
import pytest

from impaper.charwidth import char_width


@pytest.mark.parametrize("char", list(exrex.generate("[a-zA-Z]")))
def test_ascii_alphabet(char):
    assert char_width(char) == 1


@pytest.mark.parametrize("char", list(exrex.generate("[你好世界]")))
def test_chinese_alphabet(char):
    assert char_width(char) == 2
