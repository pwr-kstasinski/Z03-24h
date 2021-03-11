@echo off
set /p path=podaj sciezke
cd "%path%"
echo %path%
set a =   
call :print
pause
:print
 for %%p in (*) do echo %a% %%p
 for /D %%d in (*) do (
   echo %a% %%d
   cd %%d
   set a=   %a%
   call :print 
   cd..
 )
exit /b
