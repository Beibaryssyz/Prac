# Валидация пароля.
def validate_password(password: str) -> bool:
    if len(password) < 8: # ОШИБКА ИСПРАВЛЕНА: изменено условие длины с < 6 на < 8
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
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)): # ОШИБКА ИСПРАВЛЕНА: изменены типы аргументов с (int, int) на (int, float)
        raise TypeError("Оба аргумента должны быть числами (int или float)")
    if b == 0:
        raise ZeroDivisionError("Деление на ноль недопустимо")
    return a / b