@echo off

cd %1

set tab=    
set tabs=


:printDirectories
for %%d in (.) do (
    echo %tabs%%%~nxd
)

:: loop throught all directories in directory
:: D - directory
:: w sumie nie wiem co dzieje się z tą zmienną tabs, 
:: ale eksperymantlnie przyjmuję, że zachowywana jest jakaś lokalna wersja
for /D %%d in (./*) do (
    cd %%d
    set tabs=%tabs%^%tab%
    call :printDirectories
    cd ../
)