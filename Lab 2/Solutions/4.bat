@echo off

set fib1=0
set fib2=1
set n=%1

if %n% leq 0 (
    echo Parametr must be grater than 0
    goto end
)

echo %fib1%
if %n% == 1 goto end
echo %fib2%

:loop
    if %n% leq 2 goto end
	set /a "n=%n%-1"
	set /a num=%fib1%+%fib2%
	echo %num%
	set fib1=%fib2%
	set fib2=%num%
	goto loop	
:end