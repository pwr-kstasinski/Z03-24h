@echo off

Rem stworzylem natchniony stackoverflow'em
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

rem NOT %ERRORLEVEL% EQU 0          ?????
if %ERRORLEVEL% EQU 1 (
    echo Brak praw administratora.
)