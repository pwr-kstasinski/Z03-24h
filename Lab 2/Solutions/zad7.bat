@echo off

Rem wymagane zeby !zmienna! dzialalo
setlocal enabledelayedexpansion

set /A err = 0
Rem LSS = '<'   GTR = '>'
if %1 LSS 0 (
    set /A err = 1
)
if %1 GTR 12 (
    set /A err = 1
)

if !err! EQU 1 (
    echo Niepoprawny parametr, parametr powinien byc liczba naturalna z przedzialu 0-12
) else (
    set /A silnia = 1
    Rem for /L - The set is a sequence of numbers from start to end, by step amount.
    Rem      So (1,1,5) would generate the sequence 1 2 3 4 5 and (5,-1,1) would
    Rem      generate the sequence (5 4 3 2 1)
    for /L %%i IN (1, 1, %1) DO (
        set /A silnia *= %%i
    )
    echo !silnia!
)