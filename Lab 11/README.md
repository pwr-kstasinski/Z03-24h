## Język skryptowy

Python - [dokumentacja](https://docs.python.org/3/tutorial/index.html)   
Docker - [dokumentacja](https://docs.docker.com) | [docker-compose](https://docs.docker.com/compose/)

## Zadanie (max. 10 ptk.)

1. (2 ptk.) Przygotować obraz oparty o rozwiązanie Docker (potocznie nazywany Dockerowym) zawierający aplikacje serwera. 
   - Obraz ten ma być całkowicie zautomatyzowany, tj. aplikacja serwera ma startować wraz z uruchomieniem obrazu, bez konieczności wykonywania na obrazie dodatkowych poleceń.
   - Do utworzenia obrazu konieczne jest istnienie porawnego pliku `Dockerfile`

2. (2 ptk.) Przenieść kod komunikacji z bazą danych na rozwiązanie MySQL (np. MariaDB) lub PgSQL (np. Postgres) i połączyć je z serwerem bazy danych uruchomionym jako osobna aplikacja.
   - Serwer bazydanych może być uruchamiany z użyciem z użyciem Dockera np.: [MariaDB](https://hub.docker.com/_/mariadb) lub [postgres](https://hub.docker.com/_/postgres)

3. (2 ptk.) Umożliwić prostą konfigurację aplikacji serwera chatu za pomocą zmiennych środowiskowych
   - Aplikacja musi potrafić przyjąć dane potrzebne do połączenia z serwerem w formie tych zmiennych, więcej info: [connection-string](https://docs.sqlalchemy.org/en/14/core/engines.html)

4. (2 ptk.) Przygotować skrypt `docker-compose` odpowiedzialny za automatyczne uruchomienie całego stosu rozwiązań, czyli: serwera czatu i towarzyszącej mu bazy danych., z zastosowaniem poprawnej konfiguracji (patrz ptk. 3).

5. (max 2 ptk.) Dodać możliwość kontroli ”zdrowia” serwera chatu uruchomionego w Dockerze ([healthchecks](https://docs.docker.com/engine/reference/builder/#healthcheck))
   - Rozwiązanie musi zawierać poprawną definicje dyrektywy `HEALTHCHECK` w pliku `Dockerfile`
   - Należy dodać proste api (endpoint), którego wywołanie spowoduje że "helthcheck" serwera będzie nieprawidłowy (np. aplikacja wewnątrz obrazu zostanie zatrzymana) i w efekcie Docker Enfgine wymusi zatrzymanie i ponowne uruchomienie obrazu. 

<!-- ## Dodatkowa dokumentacja -->