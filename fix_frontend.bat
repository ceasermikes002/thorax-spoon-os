@echo off
echo.
echo ========================================
echo   Fixing Frontend Visibility on GitHub
echo ========================================
echo.

REM Check if we're in a git repository
if not exist .git (
    echo [ERROR] Not in a git repository!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

echo [Step 1] Removing frontend from Git cache...
git rm -r --cached frontend/ 2>nul
if errorlevel 1 (
    echo    ^(frontend not in cache, continuing...^)
) else (
    echo    Done!
)
echo.

echo [Step 2] Adding updated .gitignore...
git add .gitignore
echo    Done!
echo.

echo [Step 3] Adding frontend files...
git add -f frontend/app/ 2>nul && echo    Added frontend/app/
git add -f frontend/components/ 2>nul && echo    Added frontend/components/
git add -f frontend/lib/ 2>nul && echo    Added frontend/lib/
git add -f frontend/public/ 2>nul && echo    Added frontend/public/
git add -f frontend/*.json 2>nul && echo    Added frontend/*.json
git add -f frontend/*.ts 2>nul && echo    Added frontend/*.ts
git add -f frontend/*.mjs 2>nul && echo    Added frontend/*.mjs
git add -f frontend/*.js 2>nul && echo    Added frontend/*.js
echo.

echo [Step 4] Checking staged files...
git status --short
echo.

echo [Step 5] Committing changes...
git commit -m "Fix: Add frontend directory and update .gitignore" -m "- Updated .gitignore to only ignore specific frontend files (.next/, out/, .env)" -m "- Added frontend source code to repository" -m "- Frontend is now properly tracked and visible on GitHub"
echo.

echo [Step 6] Pushing to GitHub...
set /p branch="Push to which branch? (master/main) [master]: "
if "%branch%"=="" set branch=master

git push origin %branch%

if errorlevel 1 (
    echo.
    echo [ERROR] Push failed. Please check the error message above.
    echo.
    echo Common issues:
    echo   - Wrong branch name ^(try 'main' instead of 'master'^)
    echo   - Authentication required ^(check your GitHub credentials^)
    echo   - Network issues ^(check your internet connection^)
    echo.
) else (
    echo.
    echo ========================================
    echo   SUCCESS!
    echo ========================================
    echo.
    echo Frontend should now be visible on GitHub.
    echo.
    echo Check here:
    echo https://github.com/ceasermikes002/thorax-spoon-os/tree/%branch%/frontend
    echo.
    echo Note: It may take a few seconds for GitHub to update.
    echo.
)

pause

