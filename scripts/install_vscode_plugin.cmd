@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "SCRIPT_PATH=%SCRIPT_DIR%install_vscode_plugin.py"

where py >nul 2>nul
if not errorlevel 1 (
    py -3 -c "" >nul 2>nul
    if not errorlevel 1 (
        py -3 "%SCRIPT_PATH%" %*
        exit /b %ERRORLEVEL%
    )
)

where python >nul 2>nul
if not errorlevel 1 (
    python -c "" >nul 2>nul
    if not errorlevel 1 (
        python "%SCRIPT_PATH%" %*
        exit /b %ERRORLEVEL%
    )
)

where uv >nul 2>nul
if not errorlevel 1 (
    uv run --python 3 python "%SCRIPT_PATH%" %*
    exit /b %ERRORLEVEL%
)

echo ERROR: Python 3 is required to run scripts\install_vscode_plugin.py.
exit /b 1