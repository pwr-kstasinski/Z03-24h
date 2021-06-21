@echo OFF

if "%1" == "" (
	echo "You need to give a path!"
    goto :end
)

XCOPY %1 %2 /t /e

:end