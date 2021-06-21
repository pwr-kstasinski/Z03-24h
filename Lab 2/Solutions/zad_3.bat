@echo off
NET SESSION >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    ECHO Prawa administratora obecne.
) ELSE (
    ECHO Brak praw administratora.
)