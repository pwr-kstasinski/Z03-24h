@echo off
REM the script displays recursively structure directories using inside procedure
if "%1" == "" (
    echo Wrong path
    goto :end
)
setlocal
cd %1
set tab=         
:printDirectory
for %%i in (.) do (    
    echo %przerwa%%%~nxi
)
for /d %%i in (./*) do (
    cd %%i
    set przerwa=%przerwa%^%tab%
    call :printDirectory
    cd ../
    set przerwa=%przerwa:     =%
)
endLocal
:end