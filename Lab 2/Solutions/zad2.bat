@echo off
echo Podaj sciezke do folderu ktory chcesz skopiowac
set /p path1=
echo Podaj sciezke gdzie przeniesc skopiowana strukture katalogow
set /p path2=
xcopy %path1% %path2% /t /e
pause 