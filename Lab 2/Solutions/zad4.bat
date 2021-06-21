@echo off

if "%1" == "" (
	echo "You need to give a number!"
    goto :end
)

set /a N = %1

if %N% LSS 0 (
    echo "Value need to be positive!"
    goto :end
)

set /a Akk = 1
set /a val = 0
set /a temp = 0

:Fib
if %N% EQU 0 (
    echo 0
    goto :end
)
if %N% EQU 1 (
    echo %Akk%
    goto :end
)
echo %Akk%
set /a temp = %Akk%
set /a Akk += %val%  
set /a val = %temp%
set /a N -= 1
goto :Fib


:end