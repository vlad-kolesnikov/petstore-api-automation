# 🤖 Промпт для Claude Code: Генерация API Тестов

Используйте этот промпт для генерации тестов с помощью Claude Code.

---

## 📋 Базовый Промпт

```
Задача: Создать комплексный набор API тестов для Petstore API в формате JSON

Контекст проекта:
- Проект: petstore-api-automation
- PRD документ: docs/petstore-prd.md (детальное описание всех endpoints)
- Swagger спецификация: docs/petstore-swagger.json
- Test Runner: test_runner.py (готов к использованию)
- Base URL: http://localhost:3000 (через proxy)
- Authentication: API key в header (автоматически добавляется proxy)

Инфраструктура готова:
- ✅ Python test runner с поддержкой fixtures
- ✅ Proxy сервер для аутентификации
- ✅ Полная документация по использованию
- ✅ Примеры тестов с fixtures

Требования к тестам:

1. Формат: JSON (совместимый с test_runner.py)
2. Структура:
   - Разделить по категориям: Pet, Store, User
   - Создать отдельные файлы для каждой категории
   - Использовать fixtures для начальных данных
   - Включить cleanup после тестов

3. Покрытие:
   - Все основные CRUD операции
   - Позитивные сценарии (happy path)
   - Негативные сценарии (ошибки 400, 404, 405)
   - Граничные значения
   - Валидация обязательных полей

4. Организация:
   tests/
   ├── pet/
   │   ├── pet_crud.json           # Create, Read, Update, Delete
   │   ├── pet_search.json         # Find by status, tags
   │   └── pet_validation.json     # Validation errors
   ├── store/
   │   ├── store_inventory.json    # Inventory operations
   │   └── store_orders.json       # Order operations
   └── user/
       ├── user_crud.json          # User CRUD
       └── user_auth.json          # Login/Logout

5. Каждый тест должен:
   - Иметь уникальный ID (TC-001, TC-002, etc.)
   - Иметь понятное название
   - Иметь описание (что тестируется)
   - Указывать expected_status
   - Проверять ключевые поля в response (expected_response)

6. Использовать fixtures для:
   - Создания тестовых pets перед тестами
   - Создания тестовых users
   - Создания тестовых orders
   - Автоматической очистки после тестов

7. Формат JSON теста (пример):

{
  "project_name": "Petstore API - Pet CRUD Tests",
  "test_type": "backend",
  "base_url": "http://localhost:3000",
  "authentication": {
    "api_key": {
      "header": "api_key",
      "value": "special-key"
    }
  },
  "fixtures": {
    "test_pet": {
      "method": "POST",
      "path": "/pet",
      "headers": {"Content-Type": "application/json"},
      "body": {
        "name": "Test Pet",
        "photoUrls": ["https://example.com/photo.jpg"],
        "status": "available"
      }
    },
    "cleanup": [
      {
        "method": "DELETE",
        "path": "/pet/{test_pet.id}"
      }
    ]
  },
  "requirements": [
    {
      "id": "REQ-001",
      "name": "Pet CRUD Operations",
      "endpoint": "POST /pet",
      "test_cases": [
        {
          "id": "TC-001",
          "name": "Create pet with valid data",
          "description": "Should successfully create a pet with all required fields",
          "method": "POST",
          "path": "/pet",
          "headers": {"Content-Type": "application/json"},
          "body": {
            "name": "New Pet",
            "photoUrls": ["https://example.com/new-pet.jpg"],
            "status": "available"
          },
          "expected_status": 200,
          "expected_response": {
            "contains": ["id", "name", "status"]
          }
        },
        {
          "id": "TC-002",
          "name": "Create pet without required name field",
          "description": "Should return 405 validation error when name is missing",
          "method": "POST",
          "path": "/pet",
          "headers": {"Content-Type": "application/json"},
          "body": {
            "photoUrls": ["https://example.com/photo.jpg"],
            "status": "available"
          },
          "expected_status": 405
        }
      ]
    }
  ]
}

Дополнительно:
- Следуй validation rules из PRD
- Используй realistic test data
- Добавь комментарии в descriptions
- Учти все статус коды из PRD (200, 400, 404, 405)
- Используй placeholders для fixture IDs: {fixture_name.id}

Начни с создания тестов для Pet операций (самая большая категория).
Создай файл tests/pet/pet_crud.json с полным покрытием CRUD операций.
```

---

## 🎯 Пошаговый Промпт (Если хотите поэтапно)

### Шаг 1: Pet CRUD Tests

```
Создай файл tests/pet/pet_crud.json с тестами для:
1. POST /pet - Create pet (позитивные и негативные сценарии)
2. GET /pet/{petId} - Get pet (существующий, несуществующий, invalid ID)
3. PUT /pet - Update pet (существующий, несуществующий)
4. DELETE /pet/{petId} - Delete pet (существующий, несуществующий)

Используй fixtures для создания тестового pet.
Включи минимум 10 тест-кейсов.
Проверяй все validation rules из PRD.
```

### Шаг 2: Pet Search Tests

```
Создай файл tests/pet/pet_search.json с тестами для:
1. GET /pet/findByStatus - с разными статусами (available, pending, sold)
2. GET /pet/findByStatus - с множественными статусами
3. GET /pet/findByStatus - с invalid статусом
4. GET /pet/findByTags - (deprecated, но протестировать базово)

Минимум 6 тест-кейсов.
```

### Шаг 3: Store Operations Tests

```
Создай файл tests/store/store_orders.json с тестами для:
1. GET /store/inventory
2. POST /store/order - Create order
3. GET /store/order/{orderId} - Get order (ID 1-10, >10, несуществующий)
4. DELETE /store/order/{orderId}

Используй fixtures для создания test pet и test order.
Минимум 8 тест-кейсов.
```

### Шаг 4: User Operations Tests

```
Создай файл tests/user/user_crud.json с тестами для:
1. POST /user - Create user
2. GET /user/{username} - Get user
3. PUT /user/{username} - Update user
4. DELETE /user/{username} - Delete user

Используй fixtures для создания test user.
Минимум 8 тест-кейсов.
```

### Шаг 5: User Auth Tests

```
Создай файл tests/user/user_auth.json с тестами для:
1. GET /user/login - с valid credentials
2. GET /user/login - с invalid credentials
3. GET /user/logout

Используй fixtures для создания test user с известным паролем.
Минимум 4 тест-кейса.
```

---

## 🚀 Быстрый Старт Промпт

```
На основе PRD документа (docs/petstore-prd.md) создай JSON тесты для Petstore API.

1. Начни с Pet CRUD операций
2. Создай файл tests/pet/pet_crud.json
3. Используй формат совместимый с test_runner.py
4. Включи fixtures для setup/cleanup
5. Покрой позитивные и негативные сценарии
6. Проверяй все validation rules из PRD

Пример структуры теста смотри в examples/test_with_fixtures.json
```

---

## 📝 Что Попросить у Claude Code

### Вариант 1: Полный набор сразу

```
Создай полный набор API тестов для Petstore API в формате JSON:
- tests/pet/pet_crud.json
- tests/pet/pet_search.json
- tests/store/store_orders.json
- tests/user/user_crud.json
- tests/user/user_auth.json

Всего примерно 40-50 тест-кейсов покрывающих все основные операции.
Используй fixtures, validation, и следуй PRD.
```

### Вариант 2: По одному файлу

```
Создай tests/pet/pet_crud.json с комплексными CRUD тестами для Pet API.
Включи позитивные и негативные сценарии, используй fixtures.
```

Затем:
```
Отлично! Теперь создай tests/pet/pet_search.json для поисковых операций.
```

И так далее...

---

## ✅ Критерии Успеха

После генерации тестов у вас должно быть:

1. **Файлы тестов:**
   - ✅ tests/pet/pet_crud.json
   - ✅ tests/pet/pet_search.json
   - ✅ tests/store/store_orders.json
   - ✅ tests/user/user_crud.json
   - ✅ tests/user/user_auth.json

2. **Покрытие:**
   - ✅ Минимум 40 тест-кейсов
   - ✅ Все основные endpoints
   - ✅ Позитивные и негативные сценарии
   - ✅ Validation tests

3. **Качество:**
   - ✅ Fixtures используются правильно
   - ✅ Cleanup настроен
   - ✅ Expected responses определены
   - ✅ Descriptions понятные

4. **Запускаемость:**
   ```bash
   python test_runner.py tests/pet/pet_crud.json
   # Все тесты проходят или падают с понятными ошибками
   ```

---

## 🎯 После Генерации

Проверьте тесты:

```bash
# 1. Запустите proxy
npm start

# 2. В другом терминале запустите тесты
python test_runner.py tests/pet/pet_crud.json

# 3. Проверьте результаты
cat test_report.json
```

---

**Готовы создавать тесты! Просто скопируйте нужный промпт и отправьте Claude Code!** 🚀
