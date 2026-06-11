import pytest
from functions import validate_password, divide

#  Тесты для валидации пароля (вариант А)
# Параметризованный тест
@pytest.mark.parametrize("password, expected", [
    ("Password1",    True),   # TC-A1: эталонный валидный пароль
    ("Abcdefgh1234", True),   # TC-A2: длинный пароль
    ("a1b2c3d4",     True),   # TC-A3: минимально допустимый
    ("P@$$w0rd!",    True),   # TC-A12: спецсимволы разрешены
    ("short1",       False),  # TC-A4: менее 8 символов
    ("onlyletters",  False),  # TC-A5: нет цифры
    ("12345678",     False),  # TC-A6: нет буквы
    ("Pass word1",   False),  # TC-A7: есть пробел
])
def test_validate_password_parametrized(password, expected):
    assert validate_password(password) == expected

# TC-A8: граница 7 символов
def test_password_7_chars_rejected():
    assert validate_password("Passw0r") == False

# TC-A9: граница ровно 8 символов 
def test_password_8_chars_accepted():
    assert validate_password("Passw0rd") == True

# TC-A10: пустая строка
def test_password_empty_string():
    assert validate_password("") == False

# TC-A11: строка из пробелов с цифрой и буквой
def test_password_spaces_with_digit_and_letter():
    assert validate_password("        1a") == False

#  Тесты для деления чисел (вариант Б)
# Параметризованный тест
@pytest.mark.parametrize("a, b, expected", [
    (10,       2,     5.0),       # TC-B1: базовое деление
    (7,        2,     3.5),       # TC-B2: деление с остатком
    (0,        5,     0.0),       # TC-B3: ноль делимого
    (-10,      2,    -5.0),       # TC-B5: отрицательный делимый
    (10,      -2,    -5.0),       # TC-B6: отрицательный делитель
    (1,  1000000,    0.000001),   # TC-B7: очень маленький результат
    (1000000,  1,    1000000.0),  # TC-B8: очень большой делимый
    (5.5,      2.2,  2.5),        # TC-B9: оба float
])
def test_divide_parametrized(a, b, expected):
    assert divide(a, b) == pytest.approx(expected)

# TC-B4: деление на ноль ZeroDivisionError
def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

# TC-B10: строка вместо делимого TypeError
def test_divide_string_dividend_raises():
    with pytest.raises(TypeError):
        divide("abc", 2)

# TC-B11: строка вместо делителя TypeError
def test_divide_string_divisor_raises():
    with pytest.raises(TypeError):
        divide(10, "2")

# TC-B12: None вместо числа TypeError
def test_divide_none_raises():
    with pytest.raises(TypeError):
        divide(None, 2)