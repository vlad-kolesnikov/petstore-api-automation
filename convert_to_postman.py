#!/usr/bin/env python3
"""
Convert JSON test files to Postman Collection format
Generates a Postman Collection v2.1 from test JSON files
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class PostmanConverter:
    """Convert test JSON to Postman Collection format"""

    def __init__(self, test_plan_path: str):
        self.test_plan_path = test_plan_path
        self.test_plan = self._load_test_plan()

    def _load_test_plan(self) -> Dict:
        """Load test plan from JSON file"""
        try:
            with open(self.test_plan_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Test plan file not found: {self.test_plan_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in test plan: {e}")
            sys.exit(1)

    def _create_postman_request(self, test_case: Dict, base_url: str) -> Dict:
        """Convert a test case to Postman request format"""
        method = test_case.get('method', 'GET').upper()
        path = test_case.get('path', '/')
        headers = test_case.get('headers', {})
        body = test_case.get('body')

        # Build URL
        url = f"{base_url}{path}"

        # Parse query parameters from path
        url_parts = url.split('?')
        raw_url = url_parts[0]
        query_params = []

        if len(url_parts) > 1:
            query_string = url_parts[1]
            for param in query_string.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    query_params.append({
                        "key": key,
                        "value": value,
                        "description": ""
                    })

        # Build headers list
        header_list = []
        for key, value in headers.items():
            header_list.append({
                "key": key,
                "value": value,
                "type": "text"
            })

        # Add authentication header
        auth = self.test_plan.get('authentication', {})
        if 'api_key' in auth:
            api_key_config = auth['api_key']
            header_list.append({
                "key": api_key_config['header'],
                "value": api_key_config['value'],
                "type": "text"
            })

        # Build request body
        request_body = None
        if body and method in ['POST', 'PUT', 'PATCH']:
            request_body = {
                "mode": "raw",
                "raw": json.dumps(body, indent=2),
                "options": {
                    "raw": {
                        "language": "json"
                    }
                }
            }

        # Build Postman request
        postman_request = {
            "name": test_case.get('name', 'Unnamed Test'),
            "request": {
                "method": method,
                "header": header_list,
                "url": {
                    "raw": url,
                    "protocol": "http",
                    "host": raw_url.replace('http://', '').replace('https://', '').split('/')[0].split(':'),
                    "path": raw_url.split('/', 3)[3:] if '/' in raw_url.split('/', 3)[-1] else [],
                    "query": query_params
                }
            },
            "response": [],
            "event": []
        }

        # Add body if present
        if request_body:
            postman_request["request"]["body"] = request_body

        # Add description
        description_parts = []
        if test_case.get('description'):
            description_parts.append(test_case['description'])

        if test_case.get('expected_status'):
            description_parts.append(f"Expected Status: {test_case['expected_status']}")

        if test_case.get('expected_response'):
            description_parts.append(f"Expected Response: {json.dumps(test_case['expected_response'], indent=2)}")

        if description_parts:
            postman_request["request"]["description"] = "\n\n".join(description_parts)

        return postman_request

    def convert(self) -> Dict:
        """Convert test plan to Postman Collection"""
        base_url = self.test_plan.get('base_url', 'http://localhost:3000')
        project_name = self.test_plan.get('project_name', 'API Tests')

        # Build collection structure
        collection = {
            "info": {
                "name": project_name,
                "description": f"Converted from test plan: {self.test_plan_path}\nGenerated: {datetime.now().isoformat()}",
                "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
            },
            "item": []
        }

        # Process requirements (folders) and test cases (requests)
        requirements = self.test_plan.get('requirements', [])

        for req in requirements:
            req_id = req.get('id', 'UNKNOWN')
            req_name = req.get('name', 'Unnamed Requirement')
            req_description = req.get('description', '')
            test_cases = req.get('test_cases', [])

            # Create folder for each requirement
            folder = {
                "name": f"{req_id} - {req_name}",
                "description": req_description,
                "item": []
            }

            # Add test cases as requests
            for test_case in test_cases:
                request = self._create_postman_request(test_case, base_url)
                folder["item"].append(request)

            collection["item"].append(folder)

        return collection

    def save(self, output_path: str):
        """Save Postman collection to file"""
        collection = self.convert()

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(collection, f, indent=2)

        print(f"[OK] Postman collection saved to: {output_path}")
        print(f"Collection: {collection['info']['name']}")
        print(f"Folders: {len(collection['item'])}")

        total_requests = sum(len(folder['item']) for folder in collection['item'])
        print(f"Total Requests: {total_requests}")
        print(f"\nImport this file into Postman:")
        print(f"   File -> Import -> Upload Files -> {output_path}")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python convert_to_postman.py <test_plan.json> [output.json]")
        print("\nExamples:")
        print("  python convert_to_postman.py tests/pet/pet_crud.json")
        print("  python convert_to_postman.py tests/pet/pet_crud.json postman_pet_crud.json")
        sys.exit(1)

    test_plan_path = sys.argv[1]

    # Generate output filename
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    else:
        # Auto-generate output name in postman_collections folder
        input_name = Path(test_plan_path).stem
        output_path = f"postman_collections/postman_{input_name}.json"

        # Create directory if it doesn't exist
        Path("postman_collections").mkdir(exist_ok=True)

    # Convert and save
    converter = PostmanConverter(test_plan_path)
    converter.save(output_path)


if __name__ == '__main__':
    main()
