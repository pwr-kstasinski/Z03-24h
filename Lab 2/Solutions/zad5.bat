@echo off
REM the script extracts photo (extension png) with video (extension mp4)
if "%1" == "" (
    echo Wrong path
    goto :end
)
cd c:\users\polit\desktop\ffmpeg\bin\
ffmpeg -i %1 -y -update 1 photo.png 
if not %errorlevel% equ 0 (
    echo ffmpeg is unknown 
) else (
    echo Success
)
:end