Виконано:
1. За допомогою Sphinx створено документацію для застосунку.
   Для цього в основних модулях до необхідних функцій і методів класів за допомогою фреймворка Trelent додані рядки docstrings.
2. Використовуючи фреймворк Unittest модульними тестами покриті модулі репозиторію застосунку.
3. Використовуючи фреймворк pytest функціональними тестами покрито більшість функціоналу усіх маршрутів застосунку.

tests/test_main.py::test_read_main PASSED                                                         [  2%]
tests/test_route_auth.py::test_create_user PASSED                                                 [  5%]
tests/test_route_auth.py::test_repeat_create_user PASSED                                          [  8%]
tests/test_route_auth.py::test_login_user_not_confirmed PASSED                                    [ 11%]
tests/test_route_auth.py::test_login_user PASSED                                                  [ 13%]
tests/test_route_auth.py::test_login_wrong_password PASSED                                        [ 16%]
tests/test_route_auth.py::test_login_wrong_email PASSED                                           [ 19%]
tests/test_route_contacts.py::test_create_contact PASSED                                          [ 22%]
tests/test_route_contacts.py::test_get_contacts PASSED                                            [ 25%]
tests/test_route_contacts.py::test_get_contacts_mask PASSED                                       [ 27%]
tests/test_route_contacts.py::test_get_contacts_mask_notfound PASSED                              [ 30%]
tests/test_route_contacts.py::test_get_contacts_birthday_notfound PASSED                          [ 33%]
tests/test_route_contacts.py::test_get_contact PASSED                                             [ 36%]
tests/test_route_contacts.py::test_get_contact_notfound PASSED                                    [ 38%]
tests/test_route_contacts.py::test_update_contact PASSED                                          [ 41%]
tests/test_route_contacts.py::test_update_contact_notfound PASSED                                 [ 44%]
tests/test_route_contacts.py::test_get_contacts_birthday PASSED                                   [ 47%]
tests/test_route_contacts.py::test_delete_contact PASSED                                          [ 50%]
tests/test_route_contacts.py::test_repeat_delete_contact PASSED                                   [ 52%]
tests/test_route_users.py::test_read_users_me PASSED                                              [ 55%]
tests/test_unit_repository_contacts.py::TestContacts::test_create PASSED                          [ 58%]
tests/test_unit_repository_contacts.py::TestContacts::test_get_birthday_contacts_found PASSED     [ 61%]
tests/test_unit_repository_contacts.py::TestContacts::test_get_birthday_contacts_notfound PASSED  [ 63%]
tests/test_unit_repository_contacts.py::TestContacts::test_get_contact_by_id_found PASSED         [ 66%]
tests/test_unit_repository_contacts.py::TestContacts::test_get_contact_by_id_notfound PASSED      [ 69%]
tests/test_unit_repository_contacts.py::TestContacts::test_get_contacts PASSED                    [ 72%]
tests/test_unit_repository_contacts.py::TestContacts::test_get_contacts_by_mask_found PASSED      [ 75%]
tests/test_unit_repository_contacts.py::TestContacts::test_get_contacts_by_mask_notfound PASSED   [ 77%]
tests/test_unit_repository_contacts.py::TestContacts::test_remove_found PASSED                    [ 80%]
tests/test_unit_repository_contacts.py::TestContacts::test_remove_notfound PASSED                 [ 83%]
tests/test_unit_repository_contacts.py::TestContacts::test_update_found PASSED                    [ 86%]
tests/test_unit_repository_contacts.py::TestContacts::test_update_notfound PASSED                 [ 88%]
tests/test_unit_repository_users.py::TestUsers::test_confirmed_email PASSED                       [ 91%]
tests/test_unit_repository_users.py::TestUsers::test_create_user PASSED                           [ 94%]
tests/test_unit_repository_users.py::TestUsers::test_update_avatar PASSED                         [ 97%]
tests/test_unit_repository_users.py::TestUsers::test_update_token PASSED                          [100%]

coverage: platform win32, python 3.10.8-final-0

 Name      Stmts   Miss  Cover
 -----------------------------
 main.py      58     12    79%
 -----------------------------
 TOTAL        58     12    79%
 -----------------------------


Original Readme.
================
hw_rest_api - REST API для зберігання та управління контактами.
API побудований з використанням інфраструктури FastAPI та SQLAlchemy для управління базою даних.

Контакти зберігаються в базі даних PostgreSQL.

API має можливість виконувати наступні дії:

1. Зарееструватися новому користувачу з верифікацією його електронної пошти.
2. Залогінитися користувачу (пройти автентифікацію).


Зареестрованому користувачу після успішної автентифікаціі доступно:

1. Створити новий контакт.
2. Отримати список всіх контактів.
3. Отримати список контактів у яких ім'я або прізвище чи адреса електронної пошти містять заданий фрагмент.
4. Отримати список контактів з днями народження на найближчі 7 днів.
3. Отримати один контакт за ідентифікатором.
4. Оновити існуючий контакт.
5. Видалити контакт.

Додатково в застосунку:
1. Для всіх оерацій з контактами обмежена кількість запитів (не більше 10 за 1 хвилину).
2. Додано та увімкнено CORS для застосунку.
3. Реалізована можливість оновлення аватара користувача з використанням сервісу Cloudinary.
4. Реалізовано механізм кешування поточного користувача під час авторизації за допомогою бази даних Redis.
5. Усі змінні середовища зберігаються у файлі ".env". Файл доданий у ".gitignore".
6. Для запуску всіх сервісів і баз даних у застосунку використовується Docker Compose.

Поки що не реалізовано механізм скидання паролю для застосунку.
