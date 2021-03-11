@echo off
set /p path=podaj sciezke
set /p extension=podaj rozszerzenie
for %%p in ("%path%/*.%extension%") do echo %%~nxp
pause