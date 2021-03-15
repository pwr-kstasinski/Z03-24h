@echo off

net session >NUL 2>&1

IF ERRORLEVEL 1 (
    ECHO "No administrator rights"
)