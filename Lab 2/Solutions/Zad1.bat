@echo off

if "%1"=="" (
    echo Use this function like that:
    echo    Zad1.bat ^<extension^> ^<path^>^(optional^)
    goto :end
)

set EXT=%1
set PATH="."

if not "%2"=="" set PATH=%2

for %%i in (%PATH%/*) do (
    if %%~xi==%EXT% (
        echo %%i
        set FOUND=yes
    )
)

if not defined FOUND echo Nothing found.

:: pewnie za bardzo komplikuje bo mzna tez tak
:: dir %1\*%2 /B

:end