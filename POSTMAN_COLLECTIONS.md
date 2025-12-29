# Postman Collections

All Postman collections are stored in the `postman_collections/` directory.

## 📦 Available Collections

### Individual Collections (by feature)
- `postman_pet_crud.json` - 22 requests in 5 folders
- `postman_pet_search.json` - 11 requests in 2 folders
- `postman_store_orders.json` - 18 requests in 4 folders
- `postman_user_crud.json` - 18 requests in 5 folders
- `postman_user_auth.json` - 15 requests in 3 folders

### Combined Collection (all tests)
- `Petstore_API_Complete.json` - **84 requests** organized in 3 categories

**Total: 84 API requests organized by feature**

## 🚀 Quick Start

### Generate All Collections
```bash
python generate_all_postman.py
```

This generates:
- 5 individual collections (one per test file)
- 1 combined collection with all 84 requests

### Generate Single Collection
```bash
python convert_to_postman.py tests/pet/pet_crud.json
```

All collections are saved to `postman_collections/` directory.

## 🚀 How to Import into Postman

### Option 1: Import via Postman UI (Recommended: Combined Collection)
1. Open Postman
2. Click **File** → **Import**
3. Click **Upload Files**
4. Select `postman_collections/Petstore_API_Complete.json`
5. Click **Import**
6. All 84 requests will be imported organized by category

### Option 2: Drag and Drop
1. Open Postman
2. Drag `postman_collections/Petstore_API_Complete.json` into Postman
3. Collection will be imported automatically

## 🔧 What's Included

Each Postman collection contains:

- **Organized Folders**: Tests grouped by requirement ID
- **Pre-configured Headers**: API key authentication included
- **Request Bodies**: JSON payloads for POST/PUT requests
- **Query Parameters**: Properly parsed from URLs
- **Descriptions**: Test descriptions and expected results
- **Base URL**: http://localhost:3000 (proxy server)

## 📝 Collection Structure

### Combined Collection
```
Petstore API - Complete Test Suite
├── Pet Operations
│   ├── REQ-PET-001 - Pet Creation (7 requests)
│   ├── REQ-PET-002 - Pet Retrieval (4 requests)
│   ├── REQ-PET-003 - Pet Update (5 requests)
│   ├── REQ-PET-004 - Pet Partial Update (3 requests)
│   ├── REQ-PET-005 - Pet Deletion (3 requests)
│   ├── REQ-PET-SEARCH-001 - Find Pets by Status (8 requests)
│   └── REQ-PET-SEARCH-002 - Find Pets by Tags (3 requests)
├── Store Operations
│   ├── REQ-STORE-001 - Store Inventory (1 request)
│   ├── REQ-STORE-002 - Place Order (6 requests)
│   ├── REQ-STORE-003 - Get Order by ID (7 requests)
│   └── REQ-STORE-004 - Delete Order (4 requests)
└── User Operations
    ├── REQ-USER-001 - User Creation (4 requests)
    ├── REQ-USER-002 - Get User by Username (4 requests)
    ├── REQ-USER-003 - Update User (5 requests)
    ├── REQ-USER-004 - Delete User (3 requests)
    ├── REQ-USER-005 - Bulk User Creation (2 requests)
    ├── REQ-AUTH-001 - User Login (10 requests)
    ├── REQ-AUTH-002 - User Logout (2 requests)
    └── REQ-AUTH-003 - Session Management (3 requests)
```

## ⚙️ Configuration

### Base URL
All requests use: `http://localhost:3000`

Make sure your proxy server is running:
```bash
npm start
```

### Authentication
API key header is automatically included:
- **Header**: `api_key`
- **Value**: `special-key`

## 🔄 Regenerating Collections

Collections are generated from test JSON files. To regenerate after changes:

```bash
# Regenerate ALL collections (recommended)
python generate_all_postman.py

# Or regenerate a specific collection
python convert_to_postman.py tests/pet/pet_crud.json
```

Collections are saved to `postman_collections/` directory.

## 💡 Usage Tips

1. **Run Individual Requests**: Click any request and hit "Send"
2. **Run Entire Folder**: Right-click folder → "Run"
3. **Run Collection**: Use Collection Runner for all tests
4. **Save Responses**: Postman can save example responses
5. **Create Tests**: Add Postman test scripts for assertions
6. **Share Collections**: Export and share with your team

## 🆚 Postman vs Test Runner

| Feature | Postman | Test Runner |
|---------|---------|-------------|
| **Manual Testing** | ✅ Excellent | ❌ Not designed for it |
| **Automated Testing** | ⚠️ Requires scripts | ✅ Built-in |
| **Fixtures** | ❌ Manual setup | ✅ Automatic |
| **Reports** | ⚠️ Basic | ✅ HTML + JSON |
| **CI/CD** | ⚠️ Newman required | ✅ Native support |
| **Learning Curve** | ✅ Easy | ⚠️ Moderate |
| **Team Sharing** | ✅ Easy export | ✅ Git-based |

## 📚 Resources

- [Postman Documentation](https://learning.postman.com/docs/)
- [Postman Collection Format](https://schema.postman.com/)
- [Newman CLI](https://www.npmjs.com/package/newman) - Run Postman collections from command line

## 🔗 Related Files

- [convert_to_postman.py](convert_to_postman.py) - Single collection converter
- [generate_all_postman.py](generate_all_postman.py) - Generate all collections
- [postman_collections/](postman_collections/) - Output directory
- [tests/](tests/) - Source JSON test files
- [README.md](README.md) - Main project documentation

---

**Note**: The `postman_collections/` directory is gitignored to avoid clutter. Regenerate collections as needed using `python generate_all_postman.py`.
