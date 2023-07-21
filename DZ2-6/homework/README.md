1. Створення бази даних "homework.db".
    
    py create_db.py
  або
    python3 create_db.py

2. Заповнення таблиць тестовими даними.

    py seeds.py
  або
    python3 seeds.py

Талиці будуть заповнені наступним чином:

disciplines - 8 предметів;
teachers    - 5 викладачів;
groups      - 3 групи;
students    - 50 студентів;
grades      - оцінки студентів по датам за період з 01.09.2022 по 15.06.2023.

3. Виконати любий з дванадцяти запитів можна в консолі бази даних, наприклад DBeaver, або виконавши:

    py query.py
  або
    python3 query.py
