@echo OFF

if "%1" == "" (
	echo "You need to give a source!"
    goto :end
)

ffmpeg -i %1 -ss 00:00:00 -vframes 1 out.png

:end