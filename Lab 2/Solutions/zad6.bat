chcp 65001
@ECHO OFF

set sourceDir=%cd%
set tabStr=│   
set curTabStr=


cd %1
call :print
cd %sourceDir%
goto :eof


:print
for /D %%A in (*) do (
    echo %curTabStr%├───%%A
    cd %%A
    set curTabStr=%curTabStr%%tabStr%
    call :print
    cd ..
)