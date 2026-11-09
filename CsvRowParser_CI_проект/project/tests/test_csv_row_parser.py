import pytest
from interface import CsvFormatError
from csv_row_parser import CsvRowParser


@pytest.fixture
def p():
    return CsvRowParser()  # Arrange: новый объект для каждого теста


# ============ «Чёрный ящик» - по спецификации (тесты ЛР1) ============
def test_01_simple(p):
    assert p.parse_row("a,b,c") == ["a", "b", "c"]

def test_02_delimiter_in_quotes(p):
    assert p.parse_row('a,"b,c",d') == ["a", "b,c", "d"]

def test_03_escaped_quotes(p):
    assert p.parse_row('"He said ""hi""",x') == ['He said "hi"', "x"]

def test_04_empty_fields(p):
    assert p.parse_row("a,,c") == ["a", "", "c"]

def test_05_trailing_delimiter(p):
    assert p.parse_row("a,b,") == ["a", "b", ""]

def test_06_empty_line(p):
    assert p.parse_row("") == [""]

def test_07_none_raises(p):
    with pytest.raises(TypeError):
        p.parse_row(None)

def test_08_unclosed_quote(p):
    with pytest.raises(CsvFormatError):
        p.parse_row('"abc')

def test_09_custom_delimiter(p):
    assert p.parse_row('a;"b;c";d', ";") == ["a", "b;c", "d"]

def test_10_to_csv_row(p):
    assert p.to_csv_row(["a", "b,c", 'd"e']) == 'a,"b,c","d""e"'

def test_11_round_trip(p):
    src = ["x,y", 'q"z', "", " s "]
    assert p.parse_row(p.to_csv_row(src)) == src

def test_12_quoted_empty_field(p):
    assert p.parse_row('"",a') == ["", "a"]


# ============ «Белый ящик» - по веткам реализации (тесты ЛР1) ============
def test_13_spaces_not_trimmed(p):
    assert p.parse_row(" a , b ") == [" a ", " b "]

def test_14_newline_inside_quotes(p):
    assert p.parse_row('"a\nb",c') == ["a\nb", "c"]

def test_15_quote_in_unquoted_field(p):
    with pytest.raises(CsvFormatError):
        p.parse_row('ab"c,d')

def test_16_text_after_closing_quote(p):
    with pytest.raises(CsvFormatError):
        p.parse_row('"ab"c,d')

def test_17_invalid_delimiter(p):
    with pytest.raises(ValueError):
        p.parse_row("a", '"')

def test_18_only_delimiter(p):
    assert p.parse_row(",") == ["", ""]

def test_19_only_escaped_quote(p):
    assert p.parse_row('""""') == ['"']

def test_20_none_field_in_to_csv_row(p):
    assert p.to_csv_row(["a", None, "b"]) == "a,,b"


# ============ Дополнительные проверки из чек-листов (ПР2) ============
def test_21_to_csv_row_none(p):
    with pytest.raises(TypeError):
        p.to_csv_row(None)

def test_22_delimiter_cr(p):
    with pytest.raises(ValueError):
        p.parse_row("a", "\r")

def test_23_delimiter_lf(p):
    with pytest.raises(ValueError):
        p.parse_row("a", "\n")

def test_24_to_csv_row_newline(p):
    assert p.to_csv_row(["a\nb"]) == '"a\nb"'

def test_25_to_csv_row_cr(p):
    assert p.to_csv_row(["a\rb"]) == '"a\rb"'

def test_26_to_csv_row_empty_list(p):
    assert p.to_csv_row([]) == ""

def test_27_to_csv_row_spaces(p):
    assert p.to_csv_row(["a", " b"]) == "a, b"

def test_28_quoted_single_field(p):
    assert p.parse_row('"a"') == ["a"]

def test_29_quoted_first_field(p):
    assert p.parse_row('"a",b') == ["a", "b"]

def test_30_quoted_last_field(p):
    assert p.parse_row('a,"b"') == ["a", "b"]

def test_31_quoted_with_delimiter_only(p):
    assert p.parse_row('"a,b"') == ["a,b"]

def test_32_quoted_crlf(p):
    assert p.parse_row('a,"b\r\nc"') == ["a", "b\r\nc"]

def test_33_tab_delimiter(p):
    assert p.parse_row("a\tb", "\t") == ["a", "b"]

def test_34_only_quoted_empty(p):
    assert p.parse_row('""') == [""]
