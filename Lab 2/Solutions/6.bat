@echo off

set "spacer="

call :loop
goto :end

:loop
	for /D %%d in (*) do (
        echo %spacer%%%d
        cd %%d
		set "spacer=  %spacer%"
		call :loop
		cd ..
    )
:end