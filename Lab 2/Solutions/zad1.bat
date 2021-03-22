@echo off
set /p extension=Podaj rozszerzenie pliku: 
set /p path=Podaj sciezke: 
dir /b %path%\*.%extension%