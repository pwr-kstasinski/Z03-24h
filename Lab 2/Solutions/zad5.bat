@ECHO OFF

if exist .\ffmpeg.exe goto :create_thumbnail
goto :error

:create_thumbnail
.\ffmpeg.exe -i %1 -vframes 1 -ss 30 output.jpg
goto :end

:error
echo Nie znaleziono pliku ffmpeg.exe w obecnym folderze

:end