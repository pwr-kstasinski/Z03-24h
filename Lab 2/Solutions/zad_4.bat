@echo off
setlocal
IF %1 LSS 1 (
    ECHO blad danych wejsciowych.
) ELSE (

    IF %1 GEQ 1 (
       echo 0
    )

    IF %1 GEQ 2 (
       echo 1
    )

    IF %1 GEQ 3 (
        CALL :FibbFunc 0 1 %1 3
    )
)
EXIT /B %ERRORLEVEL%


:FibbFunc
:: [liczba n-2, liczba n-1, maks n , n]
setlocal
    set /A "fibN=%~1+%~2"
    echo %fibN%

    set /A "N=%~4+1"
    
    if %~3 GTR %~4 (
        
        call :FibbFunc %~2 %fibN% %~3 %N%
    )

EXIT /B 0

