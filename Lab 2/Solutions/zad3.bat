@echo off
REM the script checks, wheter admin privileges are given
if not exist %systemroot%\system32\wdi\logfiles (
    echo No admin rights
)