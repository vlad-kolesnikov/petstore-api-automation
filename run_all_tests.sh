#!/bin/bash

echo "======================================================================"
echo "  Petstore API - Running All Tests"
echo "======================================================================"
echo ""

# Check if proxy server is running
if ! curl -s http://localhost:3000/store/inventory > /dev/null 2>&1; then
    echo "⚠️  Proxy server is not running on port 3000"
    echo "Please start it with: npm start"
    echo ""
    exit 1
fi

echo "✅ Proxy server is running"
echo ""

# Initialize counters
TOTAL_PASSED=0
TOTAL_FAILED=0
TOTAL_TESTS=0

# Function to run test and capture results
run_test() {
    TEST_FILE=$1
    TEST_NAME=$2

    echo "========================================================================"
    echo "Running: $TEST_NAME"
    echo "File: $TEST_FILE"
    echo "========================================================================"
    echo ""

    # Run test and capture output
    python test_runner.py "$TEST_FILE"
    TEST_EXIT_CODE=$?

    echo ""

    # Parse results from test_report.json if it exists
    if [ -f "test_report.json" ]; then
        PASSED=$(python -c "import json; f=open('test_report.json'); data=json.load(f); print(data['summary']['passed'])")
        FAILED=$(python -c "import json; f=open('test_report.json'); data=json.load(f); print(data['summary']['failed'])")
        TOTAL=$(python -c "import json; f=open('test_report.json'); data=json.load(f); print(data['summary']['total'])")

        TOTAL_PASSED=$((TOTAL_PASSED + PASSED))
        TOTAL_FAILED=$((TOTAL_FAILED + FAILED))
        TOTAL_TESTS=$((TOTAL_TESTS + TOTAL))

        # Backup individual test report
        REPORT_NAME=$(basename "$TEST_FILE" .json)
        mv test_report.json "test_report_${REPORT_NAME}.json"
    fi

    echo ""
}

# Run Pet Tests
echo "🐾 Starting Pet Tests..."
echo ""
run_test "tests/pet/pet_crud.json" "Pet CRUD Operations"
run_test "tests/pet/pet_search.json" "Pet Search Operations"

# Run Store Tests
echo "🏪 Starting Store Tests..."
echo ""
run_test "tests/store/store_orders.json" "Store Orders Operations"

# Run User Tests
echo "👤 Starting User Tests..."
echo ""
run_test "tests/user/user_crud.json" "User CRUD Operations"
run_test "tests/user/user_auth.json" "User Authentication"

# Print final summary
echo ""
echo "======================================================================"
echo "  FINAL TEST SUMMARY"
echo "======================================================================"
echo ""
echo "Total Test Files Run:  5"
echo "Total Test Cases:      $TOTAL_TESTS"
echo "✅ Passed:             $TOTAL_PASSED"
echo "❌ Failed:             $TOTAL_FAILED"

if [ $TOTAL_TESTS -gt 0 ]; then
    PASS_RATE=$((TOTAL_PASSED * 100 / TOTAL_TESTS))
    echo "📊 Pass Rate:          ${PASS_RATE}%"
fi

echo ""
echo "Individual reports saved as:"
echo "  - test_report_pet_crud.json"
echo "  - test_report_pet_search.json"
echo "  - test_report_store_orders.json"
echo "  - test_report_user_crud.json"
echo "  - test_report_user_auth.json"
echo ""

# Exit with error if any tests failed
if [ $TOTAL_FAILED -gt 0 ]; then
    echo "⚠️  Some tests failed!"
    exit 1
else
    echo "✅ All tests passed!"
    exit 0
fi
