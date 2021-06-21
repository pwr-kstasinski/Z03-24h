@echo off

if "%1"=="" (
    echo Missing parameter. Proper params:
    echo    Zad1.bat ^<number^> 
    goto :end
)

set /A num=%1
set /A fact=1

if %num% LSS 0 (
    echo Illegal argument. Must be positive number
    goto :end
)

for /L %%i in (1,1,%num%) do set /A fact*=%%i

echo factorial: %fact%

:end