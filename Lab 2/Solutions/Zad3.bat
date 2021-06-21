@echo off

OPENFILES >NUL 2>&1
IF ERRORLEVEL 1 (
	ECHO "Script does NOT have elevated privleges"
) ELSE (
	ECHO "Script has elevated privleges"
)
PAUSE