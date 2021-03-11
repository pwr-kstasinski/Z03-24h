@echo off

if "%1"=="" (
    echo Use this function like that:
    echo    Zad2.bat ^<src^> ^<dest^>
    goto :end
)

if "%2"=="" (
    echo Use this function like that:
    echo    Zad2.bat ^<src^> ^<dest^>
    goto :end
)

xcopy %1 %2 /t /e