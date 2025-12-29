# Petstore API Automation

Comprehensive API test automation framework for Swagger Petstore API with JSON-based declarative tests and fixtures support.

## 📋 Overview

This project provides a **complete test automation framework** for the Swagger Petstore API. Tests are defined in JSON format with built-in fixtures support for data setup/cleanup, making test creation and maintenance simple and efficient.

## 🏗️ Architecture

```
┌──────────────────┐         ┌──────────────────┐
│   Python Test    │         │   Proxy Server   │
│   Runner         │────────►│   (Node.js)      │
│   (Local)        │  HTTP   │   :3000          │
└──────────────────┘         └────────┬─────────┘
                                      │
                                      │ + API Key
                                      ▼
                             ┌──────────────────┐
                             │  Petstore API    │
                             │  swagger.io/v2   │
                             └──────────────────┘
```

## ✨ Features

- **JSON Declarative Tests**: Define tests without writing code
- **Fixtures System**: Automatic setup/cleanup of test data
- **Dynamic Placeholders**: Reference fixture data in tests
- **Rich Test Reports**: JSON reports with detailed results
- **Proxy Authentication**: Automatic API key injection
- **95% API Coverage**: 73 tests across 19/20 endpoints

## 🚀 Quick Start

### Prerequisites

- **Node.js** v18+ (for proxy server)
- **Python** 3.8+ (for test runner)
- **npm** (comes with Node.js)

### 1. Install Dependencies

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Start the Proxy Server

The proxy server automatically adds API authentication headers:

```bash
npm start
```

You should see:
```
🚀 Petstore API Proxy running on http://localhost:3000
📡 Proxying to: https://petstore.swagger.io/v2
🔑 API Key: special-key
```

### 3. Run Tests

In a **new terminal window**:

```bash
# Run individual test suites
python test_runner.py tests/pet/pet_crud.json
python test_runner.py tests/pet/pet_search.json
python test_runner.py tests/store/store_orders.json
python test_runner.py tests/user/user_crud.json
python test_runner.py tests/user/user_auth.json

# Or use the convenience script to run all tests
# On Linux/Mac:
./run_all_tests.sh

# On Windows:
run_all_tests.bat
```

## 📊 Test Results

The test runner provides:

- **✅ Real-time test execution** with color-coded output
- **📈 Pass/Fail statistics** and pass rate percentage
- **🔍 Detailed error messages** for failed tests
- **📄 JSON test report** saved to `test_report.json`

### Sample Output

```
======================================================================
  TestSprite Local Test Runner
======================================================================

Project: Petstore API - Pet CRUD Operations
Test Type: backend
Base URL: http://localhost:3000
Test Plan: tests/pet/pet_crud.json

Setting up fixtures...

  [OK] Fixture 'test_pet_available' created

[REQ-PET-001] Pet Creation (POST /pet)
----------------------------------------------------------------------

  [PASS] [TC-PET-001] Create pet with all required fields
    POST http://localhost:3000/pet
    Status: 200 | Duration: 245.32ms

  [FAIL] [TC-PET-003] Create pet without required name field
    POST http://localhost:3000/pet
    Status: 200 | Duration: 198.45ms
    Error: Status code mismatch: expected 405, got 200

...

Cleaning up fixtures...

  [OK] Cleaned up: /pet/9223372036854757181

======================================================================
  Test Summary
======================================================================

Total Tests:  22
Passed:       13
Failed:       9
Pass Rate:    59.1%

Report saved to: test_report.json
```

## 📁 Project Structure

```
petstore-api-automation/
├── tests/                         # Test suites (JSON format)
│   ├── pet/
│   │   ├── pet_crud.json         # Pet CRUD operations (22 tests)
│   │   └── pet_search.json       # Pet search functionality (12 tests)
│   ├── store/
│   │   └── store_orders.json     # Store orders (18 tests)
│   ├── user/
│   │   ├── user_crud.json        # User CRUD operations (18 tests)
│   │   └── user_auth.json        # User authentication (15 tests)
│   └── TEST_SUMMARY.md           # Detailed test documentation
├── server/
│   └── proxy.js                  # Node.js proxy server
├── config/
│   └── api-config.json           # API configuration
├── docs/
│   ├── petstore-prd.md           # Product Requirements Document
│   ├── petstore-swagger.json     # Swagger/OpenAPI spec
│   └── FIXTURES_GUIDE.md         # Fixtures usage guide
├── examples/
│   └── test_with_fixtures.json   # Example test with fixtures
├── test_runner.py                # Python test runner ⭐
├── run_all_tests.sh              # Bash script to run all tests
├── run_all_tests.bat             # Windows batch script
├── requirements.txt              # Python dependencies
├── package.json                  # Node.js dependencies
├── .env.example                  # Environment variables template
├── PROJECT_OVERVIEW.md           # Complete project documentation
├── PROMPT_FOR_CLAUDE.md          # Test generation prompts
└── README.md                     # This file
```

## 🧪 Test Coverage (73 Tests, 95% API Coverage)

### Pet Management (34 tests)
- ✅ Create, Read, Update, Delete pets
- ✅ Find pets by status (available, pending, sold)
- ✅ Find pets by tags
- ✅ Update pets with form data
- ✅ Validation tests (required fields, invalid data)

### Store Operations (18 tests)
- ✅ Get inventory
- ✅ Place orders with different statuses
- ✅ Retrieve orders by ID
- ✅ Delete orders
- ✅ Order ID validation and range tests

### User Management (33 tests)
- ✅ Create, Read, Update, Delete users
- ✅ User login/logout
- ✅ Session management
- ✅ Bulk user creation (array/list)
- ✅ Authentication validation

**Not covered**: POST /pet/{petId}/uploadImage (image upload)

## 🔧 Configuration

### Environment Variables (.env)

Create a `.env` file based on `.env.example`:

```bash
# API Configuration
BASE_URL=https://petstore.swagger.io/v2
API_KEY=special-key
API_TIMEOUT=30

# Proxy Server
PROXY_PORT=3000

# Test Environment
TEST_ENV=staging
LOG_LEVEL=INFO
```

### API Configuration (config/api-config.json)

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

## 🎯 Working with Fixtures

Fixtures allow you to set up test data before tests run and clean up afterward:

```json
{
  "fixtures": {
    "test_pet": {
      "method": "POST",
      "path": "/pet",
      "body": {
        "name": "Fixture Pet",
        "status": "available"
      }
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

Use placeholders to reference fixture data:
```json
{
  "path": "/pet/{test_pet.id}",
  "body": {
    "petId": "{test_pet.id}"
  }
}
```

See [docs/FIXTURES_GUIDE.md](docs/FIXTURES_GUIDE.md) for complete documentation.

## 📝 Test Report

After execution, a detailed JSON report is saved to `test_report.json`:

```json
{
  "project_name": "Petstore API - Pet CRUD Operations",
  "test_type": "backend",
  "base_url": "http://localhost:3000",
  "timestamp": "2025-12-29T21:18:48.921175",
  "summary": {
    "total": 22,
    "passed": 13,
    "failed": 9,
    "pass_rate": 59.1
  },
  "results": [
    {
      "id": "TC-PET-001",
      "name": "Create pet with all required fields",
      "method": "POST",
      "url": "http://localhost:3000/pet",
      "passed": true,
      "message": "All validations passed",
      "response_status": 200,
      "duration_ms": 245.32
    }
  ]
}
```

## 🔍 Troubleshooting

### Port 3000 Already in Use

```bash
# Kill existing process on port 3000
# Windows:
netstat -ano | findstr :3000
taskkill /PID <pid> /F

# Linux/Mac:
lsof -ti:3000 | xargs kill -9
```

### Connection Errors

Make sure the proxy server is running:
```bash
npm start
```

Test the proxy manually:
```bash
curl http://localhost:3000/store/inventory
```

### Python Module Not Found

```bash
pip install -r requirements.txt
```

### Tests Failing Unexpectedly

Some tests may fail because the actual API behavior differs from the PRD specification:
- API validation is more lenient than documented
- Some endpoints return 200 instead of 400/404 for invalid input
- This is expected and helps identify API specification gaps

## 🔗 API Documentation

- **Petstore API**: https://petstore.swagger.io
- **Swagger Docs**: https://swagger.io/tools/swagger-editor/
- **OpenAPI Spec**: [docs/petstore-swagger.json](docs/petstore-swagger.json)
- **PRD Document**: [docs/petstore-prd.md](docs/petstore-prd.md)

## 📚 Technologies Used

- **Python 3** - Test runner implementation
- **Node.js + Express** - Proxy server
- **Requests** - HTTP client library
- **JSON** - Test plan format
- **Git** - Version control

## 🤝 Contributing

To add new tests:

1. Create or edit JSON test files in `tests/` directory
2. Follow the existing format and structure
3. Use fixtures for test data setup/cleanup
4. Run tests to verify they work
5. Update TEST_SUMMARY.md with new test details

See [PROMPT_FOR_CLAUDE.md](PROMPT_FOR_CLAUDE.md) for AI-assisted test generation.

## 📄 License

This is a test automation project for the public Swagger Petstore API.
See API documentation for terms of service.

## 🐛 Known Issues

Some tests fail due to API behavior differences from specification:
- **Validation**: API is more lenient than PRD specifies (returns 200 instead of 400/405)
- **Login Response**: Returns JSON object instead of plain string token
- **Order IDs**: Only ID 10 seems to exist in the test environment

These failures are expected and help identify gaps between API specification and implementation.

## 📖 Additional Documentation

- [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) - Complete project documentation
- [docs/FIXTURES_GUIDE.md](docs/FIXTURES_GUIDE.md) - Detailed fixtures guide
- [tests/TEST_SUMMARY.md](tests/TEST_SUMMARY.md) - All 73 test cases documented
- [NEXT_STEPS.md](NEXT_STEPS.md) - Future improvements and roadmap
- [PROMPT_FOR_CLAUDE.md](PROMPT_FOR_CLAUDE.md) - AI test generation prompts

---

**Built with Claude Code** 🤖
