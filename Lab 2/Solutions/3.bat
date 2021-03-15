@echo off

net session
IF ERRORLEVEL 1 (
    echo Not an admin
)