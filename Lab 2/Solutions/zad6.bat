@echo off

Rem ma pobierac sciezke jako parametr? w poleceniu to w sumie tego nie bylo ale pobiera

rem caly program w setLocal bo bez tego m.in. zmienia sciezke po wyjsciu z programu (+zachowuje zm. %przerwa%),
rem  a jej powtorna zmiana na koncu wywala wszystko (dlaczego? ???przywraca zmienna %cd%???)
setLocal
cd %1

:treeProcess
for %%d in (.) do (
    rem tabulator = 12 spacji
    SET tabulator=            
    echo %przerwa%%%~nxd
)
for /D %%d in ( * ) do (
    cd %%d
    set przerwa=%przerwa%%tabulator%
    call :treeProcess
    cd ..
    rem usun 12 spacji po wyjsciu z katalogu
    set przerwa=%przerwa:            =%
)

endLocal
EXIT /B
