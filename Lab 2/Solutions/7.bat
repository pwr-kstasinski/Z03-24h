@echo off

set fact=1
set n=%1

:loop
    if %n% GEQ 1 (
    set /a fact=%fact%*%n%
    set /a n=%n%-1
    goto loop
    )

echo %fact%