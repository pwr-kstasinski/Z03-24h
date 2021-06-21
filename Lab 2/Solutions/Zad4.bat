@echo off
SETLOCAL enabledelayedexpansion

SET n1=1
SET n2=0
SET tempn=0
FOR /L %%A IN (1,1,%1) DO (
	ECHO !n1!
	SET tempn=!n1!
	SET /A n1=!n2!+!tempn!
	SET n2=!tempn!
)
PAUSE