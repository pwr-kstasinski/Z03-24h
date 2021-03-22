@echo off

set n=10
set a=1
set b=1

set s= %a% %b%

:loop
	if %n% equ 0 goto print
	set /a n-=1
	set /a c=a+b
	set s=%s% %c%
	set /a a=b
	set /a b=c
	goto :loop

:print
	echo %s%

pause 