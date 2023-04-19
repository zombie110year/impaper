from impaper.typesetting import TypeSetting, IgnorableTypeSetting


def test_typesetting():
    ts = TypeSetting()
    ts.conf.line_width = 40
    ts.conf.indentation = ">>>"
    text = "1234567890" * 9
    lines = ts.wrap_text(text)
    assert lines == [
        "1234567890123456789012345678901234567890",
        ">>>1234567890123456789012345678901234567",
        ">>>8901234567890",
    ]


def test_ignorabletypesetting_iter_tokens():
    ts = IgnorableTypeSetting(labels={"<A>", "<A/>", "<B>", "<B/>"})
    text = (
        "There is a <A>pen<A/>, There is an <B>apple<B/>,"
        " There is an ... <A>apple-pen<A/>!"
    )
    tokens = list(ts.iter_tokens(text))
    assert tokens == [
        (0, "T"),
        (1, "h"),
        (2, "e"),
        (3, "r"),
        (4, "e"),
        (5, " "),
        (6, "i"),
        (7, "s"),
        (8, " "),
        (9, "a"),
        (10, " "),
        (11, "<A>"),
        (14, "p"),
        (15, "e"),
        (16, "n"),
        (17, "<A/>"),
        (21, ","),
        (22, " "),
        (23, "T"),
        (24, "h"),
        (25, "e"),
        (26, "r"),
        (27, "e"),
        (28, " "),
        (29, "i"),
        (30, "s"),
        (31, " "),
        (32, "a"),
        (33, "n"),
        (34, " "),
        (35, "<B>"),
        (38, "a"),
        (39, "p"),
        (40, "p"),
        (41, "l"),
        (42, "e"),
        (43, "<B/>"),
        (47, ","),
        (48, " "),
        (49, "T"),
        (50, "h"),
        (51, "e"),
        (52, "r"),
        (53, "e"),
        (54, " "),
        (55, "i"),
        (56, "s"),
        (57, " "),
        (58, "a"),
        (59, "n"),
        (60, " "),
        (61, "."),
        (62, "."),
        (63, "."),
        (64, " "),
        (65, "<A>"),
        (68, "a"),
        (69, "p"),
        (70, "p"),
        (71, "l"),
        (72, "e"),
        (73, "-"),
        (74, "p"),
        (75, "e"),
        (76, "n"),
        (77, "<A/>"),
        (81, "!"),
    ]
