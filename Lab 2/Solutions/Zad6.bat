@rem Skrpt przyjmuje jako argument ścieżkę do folderu który ma zostać wylistowany
@rem wypisuje jedynie strukture katalogów bez plików

@echo off
SETLOCAL enabledelayedexpansion

SET space=
FOR /L %%A IN (1,1,%2) DO (
	SET space=  !space!
)
ECHO %space% %~n1
SET /A passpacenumber= %2+1
FOR /D %%i IN ("%~f1\*") DO (

	call "%~0" "%%i" %passpacenumber%

)
