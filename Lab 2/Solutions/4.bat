@echo off
setlocal EnableDelayedExpansion

set /p n=podaj ile liczb wydrukowac
set /a a=0
set /a b=1
for /L %%p in (1,1,%n%) do (
  echo !a!
  set /a c=!a!
  set /a a=!b!
  set /a b=!a!+!c!
)
pause