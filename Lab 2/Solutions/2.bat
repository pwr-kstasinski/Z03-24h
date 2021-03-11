@echo off
set /p path=podaj sciezke z ktorej skopiowac
set /p destination=podaj gdzie skopiowac
%systemroot%\System32\xcopy "%PATH%" "%DESTINATION%" /T /E
pause