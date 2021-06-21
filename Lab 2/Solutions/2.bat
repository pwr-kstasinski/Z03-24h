@echo off

set path=%1
set des=%2

%systemroot%\System32\xcopy %path% %des% /t /e