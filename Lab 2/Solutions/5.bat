@echo off
set ffmpeg="C:\Users\Kuba\Desktop\ffmpeg\bin\ffmpeg.exe"
set /p path=podaj sciezke do pliku mp4
set /p destination=podaj gdzie zapisac obraz
%ffmpeg% -i "%path%" -vframes 1 -an -s 400x222 -ss 1 "%destination%"
pause
