@echo off

set /p N=N:

set result=1

if %N% == 0 goto one

:loop
    set /a result="%N%*%result%"
    set /a "N=%N%-1"
    if %N% == 0 goto end
    goto loop

:one
set result=1

:end
echo %result%