@echo off

if "%1"=="" (
    echo Use this like that:
    echo    Zad5.bat ^<src-movie-location^> ^<output^>(optional^)
    ::echo    size examples: [-s] [-m] [-l];
    ::echo    sdands from: small, medium, large
    goto :end
)

:: default name
for %%i IN (%1) DO (
    set OUT_NAME=%%~ni^.png
)

if not "%2"=="" (
    set OUT_NAME=%2
)

set RES="640:360"

::Na swojej maszynie nie dodawałem go do PATHs
::thumbnail szuka ramki w której następuje największa zmina obrazu. Domniemany początek sceny
ffmpeg -i %1 -vf  "thumbnail,scale=%RES%" -frames:v 1 %OUT_NAME%

if not %ERRORLEVEL%==0 (
    echo Cos poszlo nie tak.
    echo errorlevel: %ERRORLEVEL%
)

:end