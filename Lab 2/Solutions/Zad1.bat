@echo off

SET /P path= Pathname?  
ECHO.
SET /P ext= Extantion type?  
ECHO.
DIR %path%*.%ext% /B
ECHO.
PAUSE