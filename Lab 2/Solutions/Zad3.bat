@echo off
openfiles
if NOT %ERRORLEVEL% EQU 0 goto NotAdmin 
echo Stosowna informacja dla uruchomienia jako administrator
goto End
:NotAdmin 
echo Stosowna informacja dla uruchomienia bez praw dla admina
:End
pause 