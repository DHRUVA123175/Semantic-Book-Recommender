@echo off
echo 🚀 Starting Semantic Book Recommender...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "books_with_simple_categories.csv" (
    echo ❌ books_with_simple_categories.csv not found!
    echo Please make sure your book dataset is in this directory.
    pause
    exit /b 1
)

echo ✅ Python found
echo ✅ Dataset found
echo.

REM Run the application
python run.py

pause