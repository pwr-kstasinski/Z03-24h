@echo off

if "%1" == "" (
	echo "You need to give a number!"
    goto :end
)

set /a number = %1

if %number% LSS 0 (
    echo "Value need to be positive!"
    goto :end
)

set /a factorial = 1
for /L %%i in (1,1,%number%) do (
   set /A factorial *= %%i
) 
echo %factorial%

:end