@echo off
REM the script copies directory structure based on given path to directory d:\saved
REM thanks to /t /e subdirectories and empty directories are copied too
if "%1" == "" (
    echo Invalid path
    goto :end
)
xcopy %1 d:\saved /t /e
:end