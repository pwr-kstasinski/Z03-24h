@echo off

set ffmpeg="C:\Users\gosia\Downloads\ffmpeg\bin\ffmpeg.exe"
%ffmpeg% -i %1 -frames:v 1 thumbnail.jpg 