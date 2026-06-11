# TicketBook API — учебный стенд

## Запуск

1. Установить зависимости:
   pip install -r requirements.txt

2. Запустить сервер:
   uvicorn main:app --reload

3. Сервер будет доступен на: http://localhost:8000
4. Документация Swagger:         http://localhost:8000/docs

## Тестовые данные

Пользователь: user@test.com  / Test1234!
Администратор: admin@test.com / Admin1234!

Тестовые токены оплаты:
  tok_test_valid   → успешная оплата (HTTP 200)
  tok_test_decline → отказ платёжной системы (HTTP 402)

## Модули и эндпоинты

M1 Auth:
  POST /api/auth/register
  POST /api/auth/login       ← возвращает session_token
  POST /api/auth/logout

M2 Catalog:
  GET  /api/catalog/events
  GET  /api/catalog/events/{event_id}
  POST /api/catalog/events

M3 Booking:
  POST   /api/booking/create
  GET    /api/booking/{booking_id}
  GET    /api/booking
  DELETE /api/booking/{booking_id}

M4 Payment:
  POST /api/payment/pay

## Ключевые параметры передачи данных

  session_token  (M1 → M3, M3 → M4) — заголовок Authorization: Bearer <token>
  event_id       (M2 → M3)           — в теле запроса /booking/create
  booking_id     (M3 → M4)           — в теле запроса /payment/pay
  booking_status (M4 → M3)           — обновляется в базе автоматически

## Намеренный баг (для TC-INT-05)

В /api/payment/pay отсутствует проверка повторной оплаты.
При попытке оплатить уже оплаченную бронь → HTTP 500 (вместо 409).
Это и есть дефект BUG-001, который нужно найти и задокументировать.
