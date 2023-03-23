from impaper.config import Font


def test_load_font():
    font = Font()
    assert font.path == "package:///res/sarasa-mono-sc-regular.ttf"
    assert font.font is not None
    id1 = id(font.font)
    id2 = id(font.font)
    assert id1 == id2
    font.fontsize = 22
    id3 = id(font.font)
    assert id2 != id3
