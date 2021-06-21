@echo off
setlocal EnableDelayedExpansion

set /p n=podaj liczbe ktorej silnie obliczyc
set /a a=1
for /L %%p in (1,1,%n%) do (
  set /a a=!a! * %%p
)
echo !a!
pause