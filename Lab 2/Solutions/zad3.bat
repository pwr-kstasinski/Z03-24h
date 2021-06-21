@echo off
net user fedel | find /C "Administratorzy"
if "net user | find /C "Administrator"" equ 0 goto :no_rights
echo Masz prawa administratora
exit /b
:no_rights
echo Nie masz prawa administratora
exit /b