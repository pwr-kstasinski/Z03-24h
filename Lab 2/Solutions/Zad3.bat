@echo off
net user %username% | findstr /r Administrator

if %errorlevel% == 0 (
echo This is an admin account
) else (
echo This is not an admin account
)