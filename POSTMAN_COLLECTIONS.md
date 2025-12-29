# Postman Collections

This directory contains automatically generated Postman collections from our JSON test files.

## 📦 Available Collections

You can generate Postman collections for any test file using the converter:

```bash
python convert_to_postman.py tests/pet/pet_crud.json
python convert_to_postman.py tests/pet/pet_search.json
python convert_to_postman.py tests/store/store_orders.json
python convert_to_postman.py tests/user/user_crud.json
python convert_to_postman.py tests/user/user_auth.json
```

This will generate:
- `postman_pet_crud.json` - 22 requests in 5 folders
- `postman_pet_search.json` - 11 requests in 2 folders
- `postman_store_orders.json` - 18 requests in 4 folders
- `postman_user_crud.json` - 18 requests in 5 folders
- `postman_user_auth.json` - 15 requests in 3 folders

**Total: 84 API requests organized by feature**

## 🚀 How to Import into Postman

### Option 1: Import via Postman UI
1. Open Postman
2. Click **File** → **Import**
3. Click **Upload Files**
4. Select the generated `postman_*.json` file(s)
5. Click **Import**

### Option 2: Drag and Drop
1. Open Postman
2. Drag and drop the `postman_*.json` file into Postman window
3. Collections will be imported automatically

## 🔧 What's Included

Each Postman collection contains:

- **Organized Folders**: Tests grouped by requirement ID
- **Pre-configured Headers**: API key authentication included
- **Request Bodies**: JSON payloads for POST/PUT requests
- **Query Parameters**: Properly parsed from URLs
- **Descriptions**: Test descriptions and expected results
- **Base URL**: http://localhost:3000 (proxy server)

## 📝 Collection Structure

```
Petstore API - Pet CRUD Operations
├── REQ-PET-001 - Pet Creation (POST /pet)
│   ├── Create pet with all required fields
│   ├── Create pet with full details
│   └── ... (7 requests)
├── REQ-PET-002 - Pet Retrieval (GET /pet/{petId})
│   └── ... (4 requests)
└── ... (more folders)
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
# Regenerate a specific collection
python convert_to_postman.py tests/pet/pet_crud.json

# Or regenerate all collections
python convert_to_postman.py tests/pet/pet_crud.json && \
python convert_to_postman.py tests/pet/pet_search.json && \
python convert_to_postman.py tests/store/store_orders.json && \
python convert_to_postman.py tests/user/user_crud.json && \
python convert_to_postman.py tests/user/user_auth.json
```

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

- [convert_to_postman.py](convert_to_postman.py) - Converter script
- [tests/](tests/) - Source JSON test files
- [README.md](README.md) - Main project documentation

---

**Note**: Generated Postman collections (postman_*.json) are gitignored to avoid clutter. Regenerate them as needed from the source test JSON files.
