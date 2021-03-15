@echo off

set /p N=N:

set a=0
set b=1

:loop
    echo %a%

    set /a "N=%N%-1"
    if %N% == 0 goto end

	set /a buffer="%a%+%b%"
	set a=%b%
	set b=%buffer%

	goto loop
:end