@ECHO OFF
set fib1=1
set fib2=1
set i=1

:while
if %i% gtr %1 goto :end
echo %fib1%
set /A tFib=fib1+fib2
set fib1=%fib2%
set fib2=%tFib%
set /A i+=1

goto :while

:end