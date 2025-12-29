# 📊 Обзор Проекта: Petstore API Automation

## 🎯 Цель Проекта

Автоматизация тестирования REST API для Petstore (Swagger Pet Store) с использованием декларативных JSON-тестов и локального Python test runner.

---

## 📁 Структура Проекта

```
petstore-api-automation/
│
├── 📄 Документация
│   ├── README.md                      # Основная документация проекта
│   ├── PROJECT_OVERVIEW.md            # Этот файл - обзор проекта
│   ├── NEXT_STEPS.md                  # Инструкции для следующих шагов
│   └── docs/
│       ├── petstore-prd.md            # Product Requirements Document (PRD)
│       ├── petstore-swagger.json      # Swagger спецификация API
│       └── FIXTURES_GUIDE.md          # Руководство по использованию fixtures
│
├── 🔧 Инфраструктура
│   ├── server/
│   │   └── proxy.js                   # Node.js proxy сервер (порт 3000)
│   ├── config/
│   │   └── api-config.json            # Конфигурация API
│   ├── .env                           # Environment переменные (API ключи)
│   └── .env.example                   # Пример конфигурации
│
├── 🧪 Тестирование
│   ├── test_runner.py                 # Python test runner (основной движок)
│   ├── requirements.txt               # Python зависимости
│   └── examples/
│       └── test_with_fixtures.json    # Пример теста с fixtures
│
├── 📦 Конфигурация
│   ├── package.json                   # Node.js зависимости
│   ├── .gitignore                     # Git ignore правила
│   └── .claude/                       # Claude Code настройки
│
└── 🗂️ Тесты (пусто - ждут генерации!)
    └── tests/                         # Здесь будут ваши тесты
```

---

## ✅ Что Уже Реализовано

### 1. **Proxy Server (Node.js)**

**Файл:** `server/proxy.js`

**Функции:**
- ✅ Проксирование запросов к Petstore API
- ✅ Автоматическое добавление `api_key` header
- ✅ Логирование всех HTTP запросов/ответов
- ✅ CORS поддержка
- ✅ Обработка ошибок

**Запуск:**
```bash
npm start
# Доступен на http://localhost:3000
```

**Особенности:**
- Автоматически добавляет `api_key: special-key` ко всем запросам
- Проксирует на `https://petstore.swagger.io/v2`
- Выводит логи в консоль

---

### 2. **Python Test Runner**

**Файл:** `test_runner.py`

**Возможности:**

#### A. Выполнение JSON Тестов
- ✅ Загрузка test plan из JSON
- ✅ Выполнение HTTP запросов (GET, POST, PUT, DELETE)
- ✅ Валидация response (status code, body, headers)
- ✅ Цветной вывод результатов в консоль
- ✅ Генерация JSON отчета

#### B. Fixtures Support (Начальные Данные)
- ✅ **Setup:** Создание test data перед тестами
- ✅ **Placeholders:** Замена `{fixture.id}` на реальные значения
- ✅ **Cleanup:** Автоматическое удаление после тестов
- ✅ **Переиспользование:** Использование fixtures в multiple тестах

#### C. Authentication
- ✅ API Key authentication (из JSON config)
- ✅ Custom headers поддержка

#### D. Validation
- ✅ Status code проверка
- ✅ Response body fields проверка
- ✅ Response type проверка (array, object, string)
- ✅ Expected keys проверка
- ✅ Headers проверка

#### E. Reporting
- ✅ Цветной terminal output
- ✅ JSON report (`test_report.json`)
- ✅ Pass/Fail статистика
- ✅ Duration tracking

**Запуск:**
```bash
# Базовый запуск
python test_runner.py path/to/test_plan.json

# Или с примером
python test_runner.py examples/test_with_fixtures.json
```

---

### 3. **Документация**

#### A. **README.md**
- Полная инструкция по использованию
- Quick start guide
- Архитектура системы
- Примеры использования
- Troubleshooting

#### B. **FIXTURES_GUIDE.md**
- Полное руководство по fixtures
- Множество примеров
- Best practices
- Типичные ошибки
- Placeholders reference

#### C. **NEXT_STEPS.md**
- Стратегия генерации тестов
- Рекомендации по структуре
- Примеры промптов для Claude Code
- Варианты форматов тестов

#### D. **petstore-prd.md**
- Детальный PRD на 1000+ строк
- Все endpoints описаны
- Validation rules
- Error handling
- Acceptance criteria

---

## 🔑 Ключевые Компоненты

### Proxy Server (`server/proxy.js`)

```javascript
const TARGET_API = 'https://petstore.swagger.io/v2';
const API_KEY = 'special-key';

// Автоматически добавляет api_key ко всем запросам
onProxyReq: (proxyReq) => {
  proxyReq.setHeader('api_key', API_KEY);
}
```

### Test Runner (`test_runner.py`)

**Основные классы:**
- `TestRunner` - главный класс
  - `_setup_fixtures()` - создание начальных данных
  - `_execute_test()` - выполнение одного теста
  - `_validate_response()` - проверка ответа
  - `_cleanup_fixtures()` - очистка данных
  - `_resolve_placeholders()` - замена placeholders

### JSON Test Format

```json
{
  "project_name": "...",
  "base_url": "http://localhost:3000",
  "authentication": { ... },
  "fixtures": { ... },
  "requirements": [
    {
      "id": "REQ-001",
      "test_cases": [
        {
          "id": "TC-001",
          "method": "GET",
          "path": "/pet/1",
          "expected_status": 200
        }
      ]
    }
  ]
}
```

---

## 🛠️ Технологический Стек

| Компонент | Технология | Назначение |
|-----------|-----------|-----------|
| **Proxy** | Node.js + Express | Локальный прокси с auth |
| **Test Runner** | Python 3.8+ | Выполнение тестов |
| **HTTP Client** | requests | HTTP запросы |
| **Test Format** | JSON | Декларативные тесты |
| **API Target** | Petstore Swagger | Тестируемый сервис |
| **Auth** | API Key (Header) | Аутентификация |

---

## 📊 Petstore API Coverage

Из PRD документа известно **32 endpoint**:

### Pet Management (14 endpoints)
- POST /pet - Create pet
- PUT /pet - Update pet
- GET /pet/{petId} - Get pet by ID
- POST /pet/{petId} - Update pet with form
- DELETE /pet/{petId} - Delete pet
- GET /pet/findByStatus - Find by status
- GET /pet/findByTags - Find by tags (deprecated)
- POST /pet/{petId}/uploadImage - Upload image

### Store Management (8 endpoints)
- GET /store/inventory - Get inventory
- POST /store/order - Place order
- GET /store/order/{orderId} - Get order
- DELETE /store/order/{orderId} - Delete order

### User Management (10 endpoints)
- POST /user - Create user
- POST /user/createWithArray - Bulk create
- POST /user/createWithList - Bulk create
- GET /user/{username} - Get user
- PUT /user/{username} - Update user
- DELETE /user/{username} - Delete user
- GET /user/login - Login
- GET /user/logout - Logout

---

## ⚙️ Конфигурация

### Environment Variables (`.env`)

```bash
# API Configuration
BASE_URL=https://petstore.swagger.io/v2
API_TIMEOUT=30

# TestSprite Configuration (не используется для локальных тестов)
TESTSPRITE_API_KEY=sk-user-...
TESTSPRITE_PROJECT_ID=your_project_id_here

# Test Environment
TEST_ENV=staging
LOG_LEVEL=INFO
```

### API Config (`config/api-config.json`)

```json
{
  "apiName": "Petstore API",
  "baseUrl": "https://petstore.swagger.io/v2",
  "authentication": {
    "type": "apiKey",
    "headerName": "api_key",
    "value": "special-key"
  }
}
```

---

## 🎭 Примеры Использования

### Пример 1: Базовый Тест

```json
{
  "project_name": "Pet Tests",
  "base_url": "http://localhost:3000",
  "requirements": [
    {
      "id": "REQ-001",
      "test_cases": [
        {
          "id": "TC-001",
          "method": "GET",
          "path": "/store/inventory",
          "expected_status": 200
        }
      ]
    }
  ]
}
```

### Пример 2: С Fixtures

```json
{
  "fixtures": {
    "test_pet": {
      "method": "POST",
      "path": "/pet",
      "body": { "name": "Fluffy", "photoUrls": ["url"] }
    }
  },
  "requirements": [
    {
      "test_cases": [
        {
          "method": "GET",
          "path": "/pet/{test_pet.id}",
          "expected_status": 200
        }
      ]
    }
  ]
}
```

---

## 📈 Workflow

```
1. Разработчик создает JSON test plan
   ↓
2. Запускает proxy server: npm start
   ↓
3. Запускает тесты: python test_runner.py tests/plan.json
   ↓
4. Test Runner:
   - Создает fixtures (если есть)
   - Выполняет тесты
   - Валидирует ответы
   - Очищает fixtures
   - Генерирует отчет
   ↓
5. Разработчик видит результаты в консоли и test_report.json
```

---

## ❌ Что НЕ Реализовано (Ждет Вас!)

### 1. **Тесты!**
- ❌ Нет ни одного реального теста
- ❌ Папка `tests/` пуста
- ✅ Но есть инфраструктура для их запуска

### 2. **CI/CD Integration**
- ❌ GitHub Actions
- ❌ GitLab CI
- ❌ Jenkins pipeline

### 3. **Advanced Features**
- ❌ Параллельное выполнение тестов
- ❌ Retry mechanism
- ❌ Test data faker/generator
- ❌ HTML report generation
- ❌ Performance testing

---

## 🚀 Готово к Использованию

### Что работает прямо сейчас:

1. ✅ **Proxy server** - запускается и работает
2. ✅ **Test runner** - готов выполнять JSON тесты
3. ✅ **Fixtures** - полная поддержка setup/cleanup
4. ✅ **Validation** - проверка responses
5. ✅ **Reporting** - JSON и console output
6. ✅ **Documentation** - полная документация

### Что нужно сделать:

1. 📝 **Создать тесты** для всех endpoints
2. 🎯 **Организовать** по категориям (Pet, Store, User)
3. ✅ **Добавить** позитивные и негативные сценарии
4. 🔍 **Покрыть** edge cases

---

## 📚 Ресурсы

- **PRD:** [docs/petstore-prd.md](docs/petstore-prd.md)
- **Fixtures Guide:** [docs/FIXTURES_GUIDE.md](docs/FIXTURES_GUIDE.md)
- **Example:** [examples/test_with_fixtures.json](examples/test_with_fixtures.json)
- **README:** [README.md](README.md)
- **Next Steps:** [NEXT_STEPS.md](NEXT_STEPS.md)

---

## 🎓 Архитектурные Решения

### Почему JSON тесты?
- ✅ Декларативный подход
- ✅ Не требует знания Python
- ✅ Легко генерируется AI
- ✅ Легко читается и редактируется
- ✅ Версионируется в Git

### Почему Proxy Server?
- ✅ Централизованная аутентификация
- ✅ Логирование всех запросов
- ✅ Может добавлять custom headers
- ✅ CORS handling
- ✅ Изоляция от production API

### Почему Fixtures?
- ✅ Автоматическая подготовка данных
- ✅ Чистота после тестов
- ✅ Переиспользование данных
- ✅ Независимость тестов

---

**Проект готов к созданию тестов! 🎉**
