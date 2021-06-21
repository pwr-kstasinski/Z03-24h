@echo off

if "%1"=="" (
	echo "You need to give extension!"
    goto :end
)

set EXT=.%1
set PATH="."

if NOT "%2"=="" set PATH=%2

for %%i in (%PATH%/*) do (
    if %%~xi==%EXT%  (
        echo %%i
    )
)

:end
