@echo off
setlocal enabledelayedexpansion

echo ======================================================================
echo   Petstore API - Running All Tests
echo ======================================================================
echo.

REM Check if proxy server is running
curl -s http://localhost:3000/store/inventory >nul 2>&1
if errorlevel 1 (
    echo WARNING: Proxy server is not running on port 3000
    echo Please start it with: npm start
    echo.
    exit /b 1
)

echo [OK] Proxy server is running
echo.

REM Run Pet Tests
echo ====================================================================
echo Running Pet CRUD Tests...
echo ====================================================================
python test_runner.py tests\pet\pet_crud.json
if exist test_report.json move test_report.json test_report_pet_crud.json
echo.

echo ====================================================================
echo Running Pet Search Tests...
echo ====================================================================
python test_runner.py tests\pet\pet_search.json
if exist test_report.json move test_report.json test_report_pet_search.json
echo.

REM Run Store Tests
echo ====================================================================
echo Running Store Orders Tests...
echo ====================================================================
python test_runner.py tests\store\store_orders.json
if exist test_report.json move test_report.json test_report_store_orders.json
echo.

REM Run User Tests
echo ====================================================================
echo Running User CRUD Tests...
echo ====================================================================
python test_runner.py tests\user\user_crud.json
if exist test_report.json move test_report.json test_report_user_crud.json
echo.

echo ====================================================================
echo Running User Authentication Tests...
echo ====================================================================
python test_runner.py tests\user\user_auth.json
if exist test_report.json move test_report.json test_report_user_auth.json
echo.

echo ======================================================================
echo   ALL TESTS COMPLETED
echo ======================================================================
echo.
echo Individual reports saved:
echo   - test_report_pet_crud.json
echo   - test_report_pet_search.json
echo   - test_report_store_orders.json
echo   - test_report_user_crud.json
echo   - test_report_user_auth.json
echo.

pause
