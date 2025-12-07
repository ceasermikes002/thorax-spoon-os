@echo off
echo.
echo ========================================
echo   Fixing Vercel Build Error
echo ========================================
echo.

REM Check if we're in a git repository
if not exist .git (
    echo [ERROR] Not in a git repository!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

echo [Step 1] Removing frontend/lib from Git cache...
git rm -r --cached frontend/lib/ 2>nul
if errorlevel 1 (
    echo    ^(frontend/lib not in cache, continuing...^)
) else (
    echo    Done!
)
echo.

echo [Step 2] Adding updated .gitignore...
git add .gitignore
echo    Done!
echo.

echo [Step 3] Force adding frontend/lib directory...
git add -f frontend/lib/
git add -f frontend/lib/utils.ts
echo    Done!
echo.

echo [Step 4] Checking staged files...
git status --short
echo.

echo [Step 5] Committing changes...
git commit -m "Fix: Allow frontend/lib directory in Git

- Updated .gitignore to not ignore frontend/lib/
- Added frontend/lib/utils.ts (required for build)
- Fixes Vercel build error: Module not found @/lib/utils"
echo.

echo [Step 6] Pushing to GitHub...
set /p branch="Push to which branch? (master/main) [master]: "
if "%branch%"=="" set branch=master

git push origin %branch%

if errorlevel 1 (
    echo.
    echo [ERROR] Push failed. Please check the error message above.
    echo.
) else (
    echo.
    echo ========================================
    echo   SUCCESS!
    echo ========================================
    echo.
    echo frontend/lib is now in Git and Vercel should build successfully.
    echo.
    echo Next steps:
    echo 1. Go to Vercel dashboard
    echo 2. Trigger a new deployment
    echo 3. Build should succeed now!
    echo.
)

pause

