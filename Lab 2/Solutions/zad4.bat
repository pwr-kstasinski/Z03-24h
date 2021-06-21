@ECHO OFF
set fib0=0
set fib1=1
set i=1

:loop
if %i% gtr %1 exit /b
echo %fib0%
set /A temp=fib0+fib1
set fib0=%fib1%
set fib1=%temp%
set /A i+=1
goto :loop
