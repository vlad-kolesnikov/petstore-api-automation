# 🔧 Руководство по Fixtures (Начальным Данным)

## Что такое Fixtures?

**Fixtures** (фикстуры) - это начальные данные, которые создаются **перед запуском тестов** и удаляются **после их завершения**. Они нужны для:

- ✅ Создания тестовых объектов (pets, users, orders)
- ✅ Подготовки окружения для тестов
- ✅ Переиспользования данных в разных тестах
- ✅ Автоматической очистки после тестов

## 📝 Базовая Структура

```json
{
  "project_name": "Your Project",
  "base_url": "http://localhost:3000",
  "fixtures": {
    "fixture_name": {
      "method": "POST",
      "path": "/endpoint",
      "body": { ... }
    },
    "cleanup": [
      {
        "method": "DELETE",
        "path": "/endpoint/{fixture_name.id}"
      }
    ]
  },
  "requirements": [
    {
      "test_cases": [
        {
          "path": "/endpoint/{fixture_name.id}"
        }
      ]
    }
  ]
}
```

## 🎯 Примеры Использования

### Пример 1: Создание Pet Fixture

```json
{
  "fixtures": {
    "test_pet": {
      "method": "POST",
      "path": "/pet",
      "headers": {
        "Content-Type": "application/json"
      },
      "body": {
        "name": "Test Dog",
        "photoUrls": ["https://example.com/dog.jpg"],
        "status": "available"
      }
    }
  },
  "requirements": [
    {
      "test_cases": [
        {
          "id": "TC-001",
          "name": "Get pet created in fixture",
          "method": "GET",
          "path": "/pet/{test_pet.id}",
          "expected_status": 200
        }
      ]
    }
  ]
}
```

**Как работает:**
1. `test_runner.py` создает pet через `POST /pet`
2. Сохраняет response (включая `id`)
3. В тестах `{test_pet.id}` заменяется на реальный ID
4. После тестов pet удаляется (если настроен cleanup)

### Пример 2: Создание User Fixture

```json
{
  "fixtures": {
    "test_user": {
      "method": "POST",
      "path": "/user",
      "body": {
        "username": "testuser123",
        "firstName": "Test",
        "lastName": "User",
        "email": "test@example.com",
        "password": "password123"
      }
    }
  },
  "requirements": [
    {
      "test_cases": [
        {
          "id": "TC-001",
          "name": "Login with fixture user",
          "method": "GET",
          "path": "/user/login?username=testuser123&password=password123",
          "expected_status": 200
        },
        {
          "id": "TC-002",
          "name": "Get fixture user profile",
          "method": "GET",
          "path": "/user/{test_user.username}",
          "expected_status": 200
        }
      ]
    }
  ]
}
```

### Пример 3: Множественные Fixtures

```json
{
  "fixtures": {
    "pet1": {
      "method": "POST",
      "path": "/pet",
      "body": {
        "name": "Dog",
        "photoUrls": ["https://example.com/dog.jpg"],
        "status": "available"
      }
    },
    "pet2": {
      "method": "POST",
      "path": "/pet",
      "body": {
        "name": "Cat",
        "photoUrls": ["https://example.com/cat.jpg"],
        "status": "pending"
      }
    },
    "user1": {
      "method": "POST",
      "path": "/user",
      "body": {
        "username": "buyer1",
        "email": "buyer1@example.com"
      }
    }
  },
  "requirements": [
    {
      "test_cases": [
        {
          "id": "TC-001",
          "name": "Create order for pet1",
          "method": "POST",
          "path": "/store/order",
          "body": {
            "petId": "{pet1.id}",
            "quantity": 1,
            "status": "placed"
          },
          "expected_status": 200
        }
      ]
    }
  ]
}
```

## 🧹 Автоматическая Очистка (Cleanup)

### Простая Очистка

```json
{
  "fixtures": {
    "test_pet": {
      "method": "POST",
      "path": "/pet",
      "body": { ... }
    },
    "cleanup": [
      {
        "method": "DELETE",
        "path": "/pet/{test_pet.id}"
      }
    ]
  }
}
```

### Множественная Очистка

```json
{
  "fixtures": {
    "pet1": { ... },
    "pet2": { ... },
    "user1": { ... },
    "cleanup": [
      {
        "method": "DELETE",
        "path": "/pet/{pet1.id}"
      },
      {
        "method": "DELETE",
        "path": "/pet/{pet2.id}"
      },
      {
        "method": "DELETE",
        "path": "/user/buyer1"
      }
    ]
  }
}
```

## 🔗 Использование Placeholders

### Доступные Плейсхолдеры

Формат: `{fixture_name.field}`

**Примеры:**
- `{test_pet.id}` - ID созданного pet
- `{test_pet.name}` - имя pet
- `{test_pet.status}` - статус pet
- `{test_user.username}` - username пользователя
- `{test_user.email}` - email пользователя

### В Path

```json
{
  "test_cases": [
    {
      "method": "GET",
      "path": "/pet/{test_pet.id}"
    }
  ]
}
```

### В Body

```json
{
  "test_cases": [
    {
      "method": "POST",
      "path": "/store/order",
      "body": {
        "petId": "{test_pet.id}",
        "quantity": 1
      }
    }
  ]
}
```

### В Query Parameters

```json
{
  "test_cases": [
    {
      "method": "GET",
      "path": "/pet/findByTags?tags={test_pet.tags[0].name}"
    }
  ]
}
```

## 📊 Вывод при Выполнении

```bash
$ python test_runner.py examples/test_with_fixtures.json

======================================================================
  TestSprite Local Test Runner
======================================================================

Project: Petstore API - Example with Fixtures
Test Type: backend
Base URL: http://localhost:3000
Test Plan: examples/test_with_fixtures.json

Setting up fixtures...

  [OK] Fixture 'test_pet' created
  [OK] Fixture 'test_user' created

[REQ-001] Pet Operations Using Fixtures
----------------------------------------------------------------------

  [PASS] [TC-001] Get fixture pet by ID
    GET http://localhost:3000/pet/12345
    Status: 200 | Duration: 245.32ms

  [PASS] [TC-002] Update fixture pet
    PUT http://localhost:3000/pet
    Status: 200 | Duration: 198.45ms

Cleaning up fixtures...

  [OK] Cleaned up: /pet/12345
  [OK] Cleaned up: /user/fixture_user

======================================================================
  Test Summary
======================================================================

Total Tests:  2
Passed:       2
Failed:       0
Pass Rate:    100.0%
```

## 💡 Best Practices

### 1. Именование Fixtures

```json
{
  "fixtures": {
    "available_pet": { ... },    // ✅ Описательное имя
    "pending_pet": { ... },      // ✅ Указывает на состояние
    "admin_user": { ... },       // ✅ Указывает на роль
    "pet1": { ... }              // ❌ Слишком общее
  }
}
```

### 2. Минимальные Данные

```json
{
  "fixtures": {
    "test_pet": {
      "body": {
        "name": "Test Pet",
        "photoUrls": ["url"],    // ✅ Только обязательные поля
        "status": "available"
      }
      // ❌ Не добавляйте лишние поля
    }
  }
}
```

### 3. Всегда Делайте Cleanup

```json
{
  "fixtures": {
    "test_data": { ... },
    "cleanup": [              // ✅ Обязательно!
      { "method": "DELETE", "path": "..." }
    ]
  }
}
```

### 4. Группируйте Связанные Fixtures

```json
{
  "fixtures": {
    // User fixtures
    "buyer_user": { ... },
    "seller_user": { ... },

    // Pet fixtures
    "available_pet": { ... },
    "sold_pet": { ... },

    "cleanup": [ ... ]
  }
}
```

## 🚨 Частые Ошибки

### ❌ Ошибка 1: Неправильный Placeholder

```json
{
  "path": "/pet/{testpet.id}"  // ❌ Нет подчеркивания
}
```

**Правильно:**
```json
{
  "path": "/pet/{test_pet.id}"  // ✅
}
```

### ❌ Ошибка 2: Fixture Не Создается

```json
{
  "fixtures": {
    "test_pet": {
      "method": "POST",
      "path": "/pet",
      // ❌ Забыли body!
    }
  }
}
```

**Правильно:**
```json
{
  "fixtures": {
    "test_pet": {
      "method": "POST",
      "path": "/pet",
      "body": { ... }  // ✅
    }
  }
}
```

### ❌ Ошибка 3: Cleanup Без Placeholder

```json
{
  "cleanup": [
    {
      "method": "DELETE",
      "path": "/pet/123"  // ❌ Хардкод ID
    }
  ]
}
```

**Правильно:**
```json
{
  "cleanup": [
    {
      "method": "DELETE",
      "path": "/pet/{test_pet.id}"  // ✅ Использует placeholder
    }
  ]
}
```

## 🎓 Полный Пример

См. [examples/test_with_fixtures.json](../examples/test_with_fixtures.json)

## 🔧 Запуск

```bash
# С fixtures
python test_runner.py examples/test_with_fixtures.json

# Без fixtures (обычные тесты)
python test_runner.py tests/basic_tests.json
```

## 📚 Дополнительные Ресурсы

- [README.md](../README.md) - Основная документация
- [NEXT_STEPS.md](../NEXT_STEPS.md) - Следующие шаги
- [examples/](../examples/) - Примеры тестов

---

**💪 Теперь вы можете создавать мощные тесты с автоматической подготовкой данных!**
