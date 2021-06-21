@echo off
Rem wymagane zeby !zmienna! dzialalo
setlocal enabledelayedexpansion

set /A err = 0
Rem LEQ = '<='   GTR = '>'
if %1 LEQ 0 (
    set /A err = 1
)
if %1 GTR 47 (
    set /A err = 1
)

if !err! EQU 1 (
    echo Niepoprawny parametr, parametr powinien byc liczba naturalna z przedzialu 1-47
) else (
    set /A liczba_1 = 0
    set /A liczba_2 = 1
    Rem for /L - The set is a sequence of numbers from start to end, by step amount.
    Rem      So (1,1,5) would generate the sequence 1 2 3 4 5 and (5,-1,1) would
    Rem      generate the sequence (5 4 3 2 1)
    for /L %%i IN (1, 1, %1) DO (
        echo !liczba_1!
        set /A swap = !liczba_1!
        set /A liczba_1 += !liczba_2!
        set /A liczba_2 = !swap!
    )
)
