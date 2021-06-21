@echo off
set /A i=2
set /A result=1

:loop
if %i% gtr %1 goto :end
set /A result*=i
set /A i+=1
goto :loop

:end
echo %result%
exit /b