@echo OFF

if "%1"=="" (
	echo "You need to give source!"
    goto :end
)

set location=
cd %1
call :printDirectories 
goto :end

:printDirectories
for /D %%d in (*) do (
    echo %location%%%d
    cd %%d
    set location=%location%%%d\
    call :printDirectories
    cd ..    
    )
:end