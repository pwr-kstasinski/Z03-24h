@echo off

ffmpeg -i %1 -ss 00:00:01.00 -vframes 1 thumbnail.png
pause