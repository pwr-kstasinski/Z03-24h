@echo off

:: nie jestem pewien co to robi
:: ale umożliwia mi aktualizację zmiennych
:: w pętli for in
:: tutaj czytałem o tym: https://www.robvanderwoude.com/variableexpansion.php
SETLOCAL ENABLEDELAYEDEXPANSION

if "%1"=="" (
    echo Missing parameter. Proper params:
    echo    Zad1.bat ^<number^> 
    goto :end
)

if %1 LSS 0 (
    echo Illegal argument. Must be positive number
    goto :end
)

set n=%1
set l1=1
set l2=1

for /l %%g in (1,1,%n%) do (
    :: tutaj jest właśnie zastosowanie
    echo !l1!
 	set /a tmp=l1+l2
 	set /a l1=l2
	set /a l2=tmp
)
