@ECHO OFF

if "%1"=="" goto invalid_param
if 1%1 NEQ +1%1 goto invalid_param
if %1==0 goto invalid_param


set res=1

for /L %%A IN (1,1,%1) DO (
    set /a res*=%%A
)

echo %res%
goto :eof


:invalid_param
echo Param must be positive number
