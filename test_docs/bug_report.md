### Баг - репорт  shop API

### Bug-001 - [orders] заказ принимает отрицательное количество товаров

Severity: Major

Priority: High

Статус: Подтверждён на живом сервисе

Окружение: http://localhost:8000, билд N, Windows 11

**Шаги воспроизведения**:
Отправить `Post ` запрос на эндпойнт `/orders` с телом.
   ```json
  {
    "user_id": 1,
    "product_id": 3,
    "quantity": -3
  }
   ```
Ожидаемый результат: запрос откланяется со статус-кодом 422, количество дожно быть >= 1.

Фактический результат: заказ создается (статус-код 201).

Приложения:

Логи - INFO:     172.18.0.1:32860 - "POST /orders HTTP/1.1" 201 Created
    
Тело ответ сервера: ``` 201 Created ``` 
   ```json
{
    "id": 2,
    "user_id": 1,
    "product_id": 3,
    "quantity": -3
}
   ```

### Bug-002 - [orders] не проверяет остатки (stock) при заказе

Severity: Major

Priority: High

Окружение: http://localhost:8000, билд N, Windows 11

Статус: Подтверждён на живом сервисе

Предусловие: товар ``` product_id = 3``` имеет ограниченное значение

Шаги воспроизведения: Отправить `Post` запрос на эндпойнт `/orders` с телом.

   ```json
  {
    "user_id": 1,
    "product_id": 10,
    "quantity": 100000000
}
   ```

Ожидаемый результат: при количестве больше остатка заказ отклоняется, ожидаемый статус-код ответа(409).

Фактический результат:  заказ создаётся без ошибок, остаток на складе не контролируется, реальный статус-код ответа(201).

Логи - INFO:     172.18.0.1:58122 - "POST /orders HTTP/1.1" 201 Created
    
Тело ответ сервера:    ``` 201 Created ``` 
   ```json
{
    "id": 3,
    "user_id": 1,
    "product_id": 10,
    "quantity": 100000000
}
   ```


### Bug-003 - [orders] Заказ несуществующего товара роняет сервис

Severity: Critical

Priority: High

Окружение: http://localhost:8000, билд N, Windows 11

Статус: Подтверждён на живом сервисе

Предусловие: товара с ``` product_id=10000``` в каталоге нет.

Шаги воспроизведения: Отправить `Post` запрос на эндпойнт `/orders` с телом.

   ```json
  {
    "user_id": 1,
    "product_id": 10000,
    "quantity": 1
}
   ```

Ожидаемый результат: запрос отканяется со статус-кодом 404 Not Found и понятным телом ошибки - товар не найден.

Фактический результат: код ошибки 500 Internal Server Error. Сервис падает с необработанным исключением (вероятно, обращение к полю None-товара при расчёте суммы) .

### Логи
   ```
(psycopg2.errors.ForeignKeyViolation) insert or update on table "order" violates foreign key constraint "order_product_id_fkey"

DETAIL:  Key (product_id)=(10000) is not present in table "product".


[SQL: INSERT INTO "order" (user_id, product_id, quantity) VALUES (%(user_id)s, %(product_id)s, %(quantity)s) RETURNING "order".id]

[parameters: {'user_id': 1, 'product_id': 10000, 'quantity': 1}]

(Background on this error at: https://sqlalche.me/e/20/gkpj)
   ``` 

Тело ответ сервера:    ``` 500 Internal Server Error   ``` 
   ```json
{
    "id": 3,
    "user_id": 1,
    "product_id": 10,
    "quantity": 100000000
}
   ```