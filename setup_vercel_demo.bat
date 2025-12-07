@echo off
echo.
echo ========================================
echo   Thorax - Vercel Demo Setup
echo ========================================
echo.

echo This script will help you set up your Vercel deployment
echo to connect to your local backend via Ngrok.
echo.

REM Check if ngrok is installed
where ngrok >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Ngrok is not installed!
    echo.
    echo Please install ngrok:
    echo 1. Download from: https://ngrok.com/download
    echo 2. Or install via: npm install -g ngrok
    echo.
    pause
    exit /b 1
)

echo [Step 1] Checking if backend is running...
curl -s http://localhost:8000/health >nul 2>nul
if errorlevel 1 (
    echo.
    echo [WARNING] Backend is not running on localhost:8000
    echo.
    echo Please start your backend first:
    echo   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    echo.
    set /p continue="Continue anyway? (y/n): "
    if /i not "%continue%"=="y" exit /b 1
)
echo    Backend is running!
echo.

echo [Step 2] Starting Ngrok tunnel...
echo.
echo Opening ngrok in a new window...
echo.
start "Ngrok Tunnel" cmd /k "ngrok http 8000"

echo.
echo ========================================
echo   IMPORTANT: Copy Your Ngrok URL
echo ========================================
echo.
echo 1. Look at the Ngrok window that just opened
echo 2. Find the line that says "Forwarding"
echo 3. Copy the HTTPS URL (e.g., https://abc123.ngrok-free.app)
echo.
echo Example:
echo   Forwarding  https://abc123.ngrok-free.app -^> http://localhost:8000
echo              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
echo              Copy this URL
echo.
pause

echo.
echo ========================================
echo   Next Steps
echo ========================================
echo.
echo 1. Go to: https://vercel.com/dashboard
echo 2. Select project: thorax-spoon-os
echo 3. Go to: Settings -^> Environment Variables
echo 4. Add new variable:
echo    - Name: NEXT_PUBLIC_BACKEND_URL
echo    - Value: [Your ngrok HTTPS URL]
echo    - Environment: Production, Preview, Development (all)
echo 5. Click "Save"
echo 6. Go to: Deployments tab
echo 7. Click "Redeploy" on latest deployment
echo 8. Wait for build to complete
echo 9. Visit: https://thorax-spoon-os.vercel.app
echo.
echo ========================================
echo   Keep These Running During Demo
echo ========================================
echo.
echo - Backend (uvicorn)
echo - Ngrok tunnel (the window that opened)
echo.
echo Press any key to open Vercel dashboard...
pause >nul

start https://vercel.com/dashboard

echo.
echo Done! Follow the steps above to complete setup.
echo.
pause

