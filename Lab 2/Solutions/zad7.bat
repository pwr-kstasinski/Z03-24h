@echo off
REM the script counts the factorial of given number x
set /p x="Write a number to calculate its factorial: "
if %x% lss 0 (
    echo Number is less than 0
    goto :instantEnd
) 
if %x% equ 0 goto :factorial0is1
set /a result=%x%
set /a acc=%x%-1
for /l %%i in (%acc%, -1, 1) do set /a result*=%%i
goto :end
:factorial0is1
set /a result=1
:end
echo %result%
:instantEnd