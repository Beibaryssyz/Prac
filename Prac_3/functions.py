# Валидация пароля.
def validate_password(password: str) -> bool:
    if len(password) < 6: # ОШИБКА: изменено условие длины с < 8 на < 6
        return False
    if " " in password:
        return False
    if not any(c.isdigit() for c in password):
        return False
    if not any(c.isalpha() for c in password):
        return False
    return True

# Деление чисел.
def divide(a, b) -> float:
    if not isinstance(a, (int, int)) or not isinstance(b, (int, int)): # ОШИБКА: изменены типы аргументов с (int, float) на (int, int)
        raise TypeError("Оба аргумента должны быть числами (int или float)")
    if b == 0:
        raise ZeroDivisionError("Деление на ноль недопустимо")
    return a / b