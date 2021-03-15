@echo off

set /p extension=extension:
set /p path=path:

dir /b "%path%\*.%extension%"