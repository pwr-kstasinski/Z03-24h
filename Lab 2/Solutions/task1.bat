@echo off
REM the script displays files with given extension with given directory
REM %1 is the first cmd parameter -> extension
REM %2 is the second cmd parameter -> path
REM dir /b displays names of files and directories
REM with current directory
if "%1" == "" (
echo Invalid extension
goto :end
)
if "%2" == "" (
echo Invalid path
goto :end
)
dir /b %2\*%1
:end