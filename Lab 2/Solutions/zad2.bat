echo OFF
set /p source=Podaj sciezke:
set /p destination=Podaj docelowa sciezke:
xcopy %source% %destination% /s /e /t /q