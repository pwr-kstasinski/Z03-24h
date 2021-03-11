@echo off

net session >nul 2>&1
if %errorLevel% NEQ 0 (
  echo Brak uprawnien administratora
) else (
  echo Sa przyznane uprawnienia administratora
)
pause