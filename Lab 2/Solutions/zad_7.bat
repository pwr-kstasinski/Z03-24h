@echo off
setlocal
IF %1 LSS 0 (
    ECHO blad danych wejsciowych.
) ELSE (
    IF %1 EQU 0 (
       echo 1
    ) else (
        call:Silnia 1 1 %1
    )
)
EXIT /B %ERRORLEVEL%

:Silnia
setlocal
::[acc, n, max n]
set /A "acc=%~1 * %~2"
set /A "newN=%~2+1"
if %~3 GEQ %newN% (
    call:Silnia %acc% %newN% %~3
) else (
    echo %acc%
)
EXIT /B 0
