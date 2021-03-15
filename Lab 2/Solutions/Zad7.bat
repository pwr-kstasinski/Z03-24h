@rem przyjmuje liczbę jako argument
@echo off
SETLOCAL enabledelayedexpansion

SET liczba=%1
SET silnia=1

:petla
SET /A silnia=liczba*!silnia!
SET /A liczba=!liczba!-1
IF NOT !liczba! == 0 GOTO petla 

ECHO !silnia!
PAUSE 
