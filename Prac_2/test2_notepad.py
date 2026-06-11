import os
import pytest

# ─── Вспомогательные функции (имитация логики tk-notepad) ───

def save_file(filepath, text):
    """Имитирует File → Save As"""
    with open(filepath, "w+", encoding="utf-8") as f:
        f.write(text)

def open_file(filepath):
    """Имитирует File → Open"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл не найден: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

# ─── Тесты ───

# TC-01: Сохранение файла с текстом
def test_save_file_creates_file():
    save_file("test_tc01.txt", "Привет")
    assert os.path.exists("test_tc01.txt"), "FAIL: файл не создан"
    os.remove("test_tc01.txt")

# TC-02: Сохранение пустого файла
def test_save_empty_file():
    save_file("test_tc02.txt", "")
    assert os.path.exists("test_tc02.txt"), "FAIL: пустой файл не создан"
    os.remove("test_tc02.txt")

# TC-03: Перезапись файла
def test_save_overwrites_content():
    save_file("test_tc03.txt", "Старый текст")
    save_file("test_tc03.txt", "Новый текст")
    content = open_file("test_tc03.txt")
    assert content == "Новый текст", "FAIL: содержимое не обновлено"
    os.remove("test_tc03.txt")

# TC-06: Открытие существующего файла
def test_open_existing_file():
    save_file("test_tc06.txt", "Тестовый текст")
    content = open_file("test_tc06.txt")
    assert content == "Тестовый текст", "FAIL: содержимое не совпадает"
    os.remove("test_tc06.txt")

# TC-09: Открытие несуществующего файла — ожидаем FileNotFoundError
def test_open_nonexistent_file_raises_error():
    with pytest.raises(FileNotFoundError):
        open_file("не_существует.txt")
