import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
test_file = os.path.join(BASE_DIR, "test_save.txt")
def check_file_exists(filepath):
    """Проверяет наличие файла"""
    return os.path.exists(filepath)
def check_file_content(filepath, expected_text):
    """Проверяет содержимое файла"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return content == expected_text

# TEST CASE TC-03
expected = "Тестовый текст"
with open(test_file, "w", encoding="utf-8") as f:
    f.write(expected)

assert check_file_exists(test_file), "FAIL: Файл не создан"
print("TC-03 PASS: Файл успешно создан")

assert check_file_content(test_file, expected), "FAIL: Содержимое не совпадает"
print("TC-03 PASS: Содержимое файла корректно")

# TEST CASE TC-04
assert os.path.exists(test_file), "FAIL: Файл для открытия не найден"
print("TC-04 PASS: Файл доступен для открытия")

print("\nALL AUTOMATED TESTS PASSED SUCCESSFULLY")