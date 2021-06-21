## Język skryptowy

Python - [dokumentacja](https://docs.python.org/3/tutorial/index.html)   
Alternatywnie JavaScript/TypeScript dla zaawansowanych - [TypeScript](https://www.typescriptlang.org) + [React](https://reactjs.org) lub [Angular](https://angular.io) lub [Vue](https://vuejs.org)   

## Zadanie (max. 10 ptk.)

Napisz prostą aplikację klient – serwer umożliwiającą komunikację tekstową pomiędzy klientami za pośrednictwem serwera.

Kontynuacja [Lab 8](../Lab-8/README.md)

### Wymagania

0. (wymaganie podstawowe) Aplkacja realizuje wszystkie wymagania z Lab 8 (chyba że uzgodniono inaczej) 

1. (4 ptk.) Dane klientów powinny być przechowywane w na serwerze w bazie danych (np. MySQL).
    - wysyłane wiadomości
    - dane logowania
    - etc.

2. (1 ptk.) Połaczenie z bazą danych oraz mapowanie encji jest obsługiwane przez bilbiotekę ORM, np. SQL Alchemy.

3. (1 ptk.) Aplikacja umożliwia rejestracje nowego klienta (zdefinowanie loginu/nicku i hasła).

4. (1 ptk.) Aplikacja umożliwia zalogowanie się klienta za pomocą loginu i hasła.

5. (1 ptk.) Aplikacja umożliwia podgląd listy zalogowanych użytkowników.

6. (max 2 ptk.) Aplikacja konwersację 
   - (1 ptk. - Wymaganie z Lab 8) Wszytskich
   - (1 ptk.) z wybranym użytkownikiem.


### Przykłady bibliotek ORM:
   - [SQLAlchemy](https://www.sqlalchemy.org) - [GitHub](https://github.com/zzzeek/sqlalchemy)
   - [peewee](http://docs.peewee-orm.com/en/latest/) - [GitHub](https://github.com/coleifer/peewee)
   - [Django ORM](http://www.djangoproject.com) - [GitHub](https://github.com/django/django)
   - [Pony](https://ponyorm.org) - [GitHub](https://github.com/ponyorm/pony)
   - [sqlobject](http://sqlobject.org)
   - [Tortoise ORM](https://tortoise-orm.readthedocs.io/en/latest/)