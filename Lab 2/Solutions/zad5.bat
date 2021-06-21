@echo off

rem pobranie nazwy pliku wideo (bez rozszerzenia)
for %%d in (%1) do set nazwaPliku=%%~nd

rem konkatenacja nazwy miniatury
set nazwaPliku=miniatura_%nazwaPliku%.png

rem (cicho)                hh:mm:ss:msec    - klatka z tego czasu bedzie obrazem
>nul 2>&1 ffmpeg -i %1 -ss 00:00:00.001 -vframes 1 %nazwaPliku%

if NOT %ERRORLEVEL%  EQU 0 (
    echo Niepowodzenie. Nie znaleziono programu ffmpeg. Dodaj go do listy $PATH.
) else (
    echo Sukces. Utworzono plik '%nazwaPliku%'.
)
rem C:\Users\Ja\Desktop\ffmpeg-4.3.2-2021-02-27-essentials_build\bin
