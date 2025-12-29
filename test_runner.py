#!/usr/bin/env python3
"""
Local Test Runner for TestSprite Tests
Executes JSON-based API tests locally
"""

import json
import sys
import requests
from typing import Dict, List, Any
from datetime import datetime
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class TestRunner:
    """Executes TestSprite JSON test plans locally"""

    def __init__(self, test_plan_path: str):
        self.test_plan_path = test_plan_path
        self.test_plan = self._load_test_plan()
        self.base_url = self.test_plan.get('base_url', 'http://localhost:3000')
        self.auth = self.test_plan.get('authentication', {})
        self.fixtures = self.test_plan.get('fixtures', {})
        self.fixture_data = {}  # Store created fixture data
        self.results = {
            'passed': 0,
            'failed': 0,
            'total': 0,
            'details': []
        }

    def _load_test_plan(self) -> Dict:
        """Load test plan from JSON file"""
        try:
            with open(self.test_plan_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"{Colors.RED}Error: Test plan file not found: {self.test_plan_path}{Colors.RESET}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"{Colors.RED}Error: Invalid JSON in test plan: {e}{Colors.RESET}")
            sys.exit(1)

    def _build_headers(self, test_headers: Dict = None) -> Dict:
        """Build request headers including authentication"""
        headers = {}

        # Add auth headers
        if 'api_key' in self.auth:
            api_key_config = self.auth['api_key']
            headers[api_key_config['header']] = api_key_config['value']

        # Add test-specific headers
        if test_headers:
            headers.update(test_headers)

        return headers

    def _setup_fixtures(self):
        """Setup test fixtures by creating initial data"""
        if not self.fixtures:
            return

        print(f"{Colors.BOLD}{Colors.YELLOW}Setting up fixtures...{Colors.RESET}\n")

        for fixture_name, fixture_config in self.fixtures.items():
            # Skip cleanup - it's not a fixture to create
            if fixture_name == 'cleanup':
                continue

            method = fixture_config.get('method', 'POST').upper()
            path = fixture_config.get('path')
            body = fixture_config.get('body')
            headers = self._build_headers(fixture_config.get('headers'))

            url = f"{self.base_url}{path}"

            try:
                if method == 'POST':
                    response = requests.post(url, headers=headers, json=body, timeout=10)
                elif method == 'PUT':
                    response = requests.put(url, headers=headers, json=body, timeout=10)
                else:
                    print(f"  {Colors.YELLOW}[SKIP] Fixture '{fixture_name}': Unsupported method {method}{Colors.RESET}")
                    continue

                if response.status_code in [200, 201]:
                    print(f"  {Colors.GREEN}[OK] Fixture '{fixture_name}' created{Colors.RESET}")
                    # Store response data for later use
                    try:
                        self.fixture_data[fixture_name] = response.json()
                    except:
                        self.fixture_data[fixture_name] = {'status': 'created'}
                else:
                    print(f"  {Colors.RED}[FAIL] Fixture '{fixture_name}': Status {response.status_code}{Colors.RESET}")
            except Exception as e:
                print(f"  {Colors.RED}[ERROR] Fixture '{fixture_name}': {str(e)}{Colors.RESET}")

        print()

    def _cleanup_fixtures(self):
        """Cleanup test fixtures by deleting created data"""
        cleanup = self.fixtures.get('cleanup', [])
        if not cleanup:
            return

        print(f"\n{Colors.BOLD}{Colors.YELLOW}Cleaning up fixtures...{Colors.RESET}\n")

        for cleanup_config in cleanup:
            method = cleanup_config.get('method', 'DELETE').upper()
            path = cleanup_config.get('path')
            headers = self._build_headers(cleanup_config.get('headers'))

            # Replace placeholders with fixture data
            if path and '{' in path:
                for fixture_name, data in self.fixture_data.items():
                    if isinstance(data, dict) and 'id' in data:
                        path = path.replace(f'{{{fixture_name}.id}}', str(data['id']))

            url = f"{self.base_url}{path}"

            try:
                if method == 'DELETE':
                    response = requests.delete(url, headers=headers, timeout=10)
                    if response.status_code in [200, 204]:
                        print(f"  {Colors.GREEN}[OK] Cleaned up: {path}{Colors.RESET}")
                    else:
                        print(f"  {Colors.YELLOW}[WARN] Cleanup failed: {path} (Status {response.status_code}){Colors.RESET}")
            except Exception as e:
                print(f"  {Colors.RED}[ERROR] Cleanup failed: {path} - {str(e)}{Colors.RESET}")

        print()

    def _resolve_placeholders(self, value: Any) -> Any:
        """Replace placeholders in test data with fixture values"""
        if isinstance(value, str):
            # Replace {fixture_name.field} with actual values
            for fixture_name, data in self.fixture_data.items():
                if isinstance(data, dict):
                    for field, field_value in data.items():
                        placeholder = f'{{{fixture_name}.{field}}}'
                        if placeholder in value:
                            value = value.replace(placeholder, str(field_value))
        elif isinstance(value, dict):
            return {k: self._resolve_placeholders(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self._resolve_placeholders(item) for item in value]

        return value

    def _validate_response(self, response: requests.Response, expected: Dict) -> tuple[bool, str]:
        """Validate response against expected criteria"""
        errors = []

        # Check status code
        expected_status = expected.get('expected_status')
        if expected_status and response.status_code != expected_status:
            errors.append(
                f"Status code mismatch: expected {expected_status}, got {response.status_code}"
            )

        # Check response body
        expected_response = expected.get('expected_response', {})

        if expected_response:
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                response_data = response.text

            # Check if response contains expected fields
            if 'contains' in expected_response and isinstance(response_data, dict):
                for field in expected_response['contains']:
                    if field not in response_data:
                        errors.append(f"Response missing expected field: {field}")

            # Check if response is expected type
            if 'type' in expected_response:
                expected_type = expected_response['type']
                if expected_type == 'array' and not isinstance(response_data, list):
                    errors.append(f"Response type mismatch: expected array, got {type(response_data).__name__}")
                elif expected_type == 'object' and not isinstance(response_data, dict):
                    errors.append(f"Response type mismatch: expected object, got {type(response_data).__name__}")
                elif expected_type == 'string' and not isinstance(response_data, str):
                    errors.append(f"Response type mismatch: expected string, got {type(response_data).__name__}")

            # Check if response contains expected keys
            if 'contains_keys' in expected_response and isinstance(response_data, dict):
                for key in expected_response['contains_keys']:
                    if key not in response_data:
                        errors.append(f"Response missing expected key: {key}")

        # Check expected headers
        expected_headers = expected.get('expected_headers', {})
        for header, expected_type in expected_headers.items():
            if header not in response.headers:
                errors.append(f"Response missing expected header: {header}")

        if errors:
            return False, '; '.join(errors)
        return True, "All validations passed"

    def _execute_test(self, test_case: Dict) -> Dict:
        """Execute a single test case"""
        test_id = test_case.get('id', 'UNKNOWN')
        test_name = test_case.get('name', 'Unnamed Test')
        method = test_case.get('method', 'GET').upper()
        path = self._resolve_placeholders(test_case.get('path', '/'))
        headers = self._build_headers(test_case.get('headers'))
        body = self._resolve_placeholders(test_case.get('body'))

        url = f"{self.base_url}{path}"

        result = {
            'id': test_id,
            'name': test_name,
            'method': method,
            'url': url,
            'passed': False,
            'message': '',
            'response_status': None,
            'duration_ms': 0
        }

        try:
            start_time = datetime.now()

            # Make HTTP request
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=body, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, json=body, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds() * 1000

            result['response_status'] = response.status_code
            result['duration_ms'] = round(duration, 2)

            # Validate response
            passed, message = self._validate_response(response, test_case)
            result['passed'] = passed
            result['message'] = message

        except requests.exceptions.Timeout:
            result['message'] = "Request timeout (>10s)"
        except requests.exceptions.ConnectionError:
            result['message'] = "Connection error - is the server running?"
        except Exception as e:
            result['message'] = f"Error: {str(e)}"

        return result

    def _print_test_result(self, result: Dict):
        """Print formatted test result"""
        status_icon = f"{Colors.GREEN}[PASS]{Colors.RESET}" if result['passed'] else f"{Colors.RED}[FAIL]{Colors.RESET}"
        status_text = f"{Colors.GREEN}PASS{Colors.RESET}" if result['passed'] else f"{Colors.RED}FAIL{Colors.RESET}"

        print(f"  {status_icon} [{result['id']}] {result['name']}")
        print(f"    {result['method']} {result['url']}")

        if result['response_status']:
            status_color = Colors.GREEN if result['passed'] else Colors.RED
            print(f"    Status: {status_color}{result['response_status']}{Colors.RESET} | Duration: {result['duration_ms']}ms")

        if not result['passed']:
            print(f"    {Colors.RED}Error: {result['message']}{Colors.RESET}")

        print()

    def run_all_tests(self):
        """Execute all tests in the test plan"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}  TestSprite Local Test Runner{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}\n")

        print(f"{Colors.BOLD}Project:{Colors.RESET} {self.test_plan.get('project_name', 'Unknown')}")
        print(f"{Colors.BOLD}Test Type:{Colors.RESET} {self.test_plan.get('test_type', 'Unknown')}")
        print(f"{Colors.BOLD}Base URL:{Colors.RESET} {self.base_url}")
        print(f"{Colors.BOLD}Test Plan:{Colors.RESET} {self.test_plan_path}\n")

        # Setup fixtures before running tests
        self._setup_fixtures()

        requirements = self.test_plan.get('requirements', [])

        for req in requirements:
            req_id = req.get('id', 'UNKNOWN')
            req_name = req.get('name', 'Unnamed Requirement')
            test_cases = req.get('test_cases', [])

            print(f"{Colors.BOLD}{Colors.BLUE}[{req_id}] {req_name}{Colors.RESET}")
            print(f"{Colors.BLUE}{'-'*70}{Colors.RESET}\n")

            for test_case in test_cases:
                result = self._execute_test(test_case)
                self._print_test_result(result)

                self.results['total'] += 1
                if result['passed']:
                    self.results['passed'] += 1
                else:
                    self.results['failed'] += 1

                self.results['details'].append(result)

        # Cleanup fixtures after all tests
        self._cleanup_fixtures()

        self._print_summary()

        # Return exit code for main() to use
        return 1 if self.results['failed'] > 0 else 0

    def _print_summary(self):
        """Print test execution summary"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}  Test Summary{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}\n")

        total = self.results['total']
        passed = self.results['passed']
        failed = self.results['failed']
        pass_rate = (passed / total * 100) if total > 0 else 0

        print(f"{Colors.BOLD}Total Tests:{Colors.RESET}  {total}")
        print(f"{Colors.GREEN}Passed:{Colors.RESET}       {passed}")
        print(f"{Colors.RED}Failed:{Colors.RESET}       {failed}")
        print(f"{Colors.BOLD}Pass Rate:{Colors.RESET}    {pass_rate:.1f}%\n")

        if failed > 0:
            print(f"{Colors.BOLD}{Colors.RED}Failed Tests:{Colors.RESET}")
            for result in self.results['details']:
                if not result['passed']:
                    print(f"  • [{result['id']}] {result['name']}")
                    print(f"    {Colors.RED}{result['message']}{Colors.RESET}")
            print()

    def save_report(self, output_path: str = 'test_report.json'):
        """Save test results to JSON file"""
        report = {
            'project_name': self.test_plan.get('project_name'),
            'test_type': self.test_plan.get('test_type'),
            'base_url': self.base_url,
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total': self.results['total'],
                'passed': self.results['passed'],
                'failed': self.results['failed'],
                'pass_rate': (self.results['passed'] / self.results['total'] * 100) if self.results['total'] > 0 else 0
            },
            'results': self.results['details']
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        print(f"{Colors.GREEN}Report saved to: {output_path}{Colors.RESET}\n")


def main():
    """Main entry point"""
    # Default test plan path
    default_path = Path(__file__).parent / 'testsprite_tests' / 'testsprite_backend_test_plan.json'

    # Check if custom path provided
    test_plan_path = sys.argv[1] if len(sys.argv) > 1 else str(default_path)

    # Create and run test runner
    runner = TestRunner(test_plan_path)
    exit_code = runner.run_all_tests()
    runner.save_report('test_report.json')

    # Exit with appropriate code
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
