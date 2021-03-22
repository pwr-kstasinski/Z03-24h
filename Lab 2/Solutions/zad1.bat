@echo off
echo Podaj sciezke
set /p path=
echo Podaj rozszerzenie
set /p extension=
cd %path%
dir *.%extension% /b 
pause 