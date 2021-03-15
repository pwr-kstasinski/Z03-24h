@echo off
set path=%1
set ind =   

cd %path%
call :loop
goto :end

:loop
	for /D %%d in (*) do (
        echo %ind% %%d
        cd %%d
		set ind=   %ind%
		call :loop
		cd ..	
)
:end