Консольна утиліта запиту курсів валют.

Виконує запит курсів валют в окремих сесіях за кожен день паралельно.


Запуск утиліти:
    
    py main.py [[<кількість днів від поточного>] [<список валют через кому або пробіл>]]
  або
    python3 main.py [[<кількість днів від поточного>] [<список валют через кому або пробіл>]]

    <кількість днів від поточного> - не быльше 10-и днів.

    Наприклад:

        py main.py
            виведуться курси EUR та USD за поточну дату

        py main.py 3
            виведуться курси EUR та USD за поточну, вчорашню та позавчорашню дати

        py main.py CAD, USD
            виведуться курси CAD та USD за поточну дату

        py main.py 2 CAD USD
            виведуться курси CAD та USD за поточну та вчорашню дати

Курси валют зберігаються у файлі  rates.json
