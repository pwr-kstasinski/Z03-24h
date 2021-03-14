@echo off
REM the script disaplays first [Nth] numbers of Fibonacci sequence
setlocal enabledelayedexpansion
if "%1" leq "0" (
echo The parameter must be greater than 0
goto :end
)
echo First %1 numbers of Fibonacci sequence:
set /a firstNumber=0
set /a secondNumber=1
for /l %%i in (1, 1, %1%) do (
echo !firstNumber!
set /a accumulator=!firstNumber!+!secondNumber!
set /a firstNumber=!secondNumber!
set /a secondNumber=!accumulator!
)
:end