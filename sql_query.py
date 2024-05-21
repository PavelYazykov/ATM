import sqlite3
import csv
import datetime


now_date = datetime.datetime.utcnow().strftime('%H:%M - %d.%m.%Y')


class Sql_atm:

    @staticmethod
    def create_table():
        """Создание таблицы Users_data"""
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS Users_data(
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                Number_card INTEGER NOT NULL,
                Pin_code INTEGER NOT NULL,
                Balance INTEGER NOT NULL);
            """)

    @staticmethod
    def insert_user(data_users):
        """Создание нового пользователя"""
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute("""INSERT INTO Users_data(Number_card, Pin_code, Balance)
                VALUES(?, ?, ?);""", data_users)

    @staticmethod
    def input_card(number_card):
        """Ввод и проверка карты"""
        try:
            with sqlite3.connect('atm.db') as db:
                cur = db.cursor()
                cur.execute(f"""SELECT Number_card FROM Users_data WHERE Number_card = {number_card}""")
                result_card = cur.fetchone()
                if result_card is None:
                    print('Введен неизвестный номер карты')
                    return False
                else:
                    print(f'Введен номер карты: {number_card}')
                    return True
        except:
            print('Введен неизвестный номер карты')

    @staticmethod
    def input_code(number_card):
        """Ввод и проверка пин кода"""
        pin_code = input('Введите пин код: ')
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute(f"""SELECT Pin_code FROM Users_data WHERE Number_card = {number_card} """)
            result_code = cur.fetchone()
            input_pin = result_code[0]
            try:
                if input_pin == int(pin_code):
                    print('Введен верный пин код')
                    return True
                else:
                    print('Введен некорректный пин код')
                    return False
            except:
                print('Введен некорректный пин код')

    @staticmethod
    def info_balance(number_card):
        """Вывод на экран баланса карты"""
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute(f"""SELECT Balance FROM Users_data WHERE Number_card = {number_card}""")
            result = cur.fetchone()
            balance_card = result[0]
            print(f'Баланс карты: {balance_card}')

    @staticmethod
    def withdrew_money(number_card):
        """Снятие наличных"""
        amount = input('Введите сумму: ')
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            cur.execute(f"""SELECT Balance FROM Users_data WHERE Number_card = {number_card}""")
            result_balance = cur.fetchone()
            balance_card = result_balance[0]
            try:
                if int(amount) > balance_card:
                    print('Недостаточно средств')
                elif balance_card > int(amount) and amount.isdigit():
                    cur.execute(f"""UPDATE Users_data SET Balance = Balance - {amount} WHERE Number_card =
                        {number_card};""")
                    db.commit()
                    print(f'{amount} выдана')
                    return True
                else:
                    print('Попытка выполнить некорректное действие')
            except:
                print('Попытка выполнить некорректное действие')
                return False

    @staticmethod
    def depositing_money(number_card):
        """внесение денежных средств"""
        amount = input('какую сумму хотите внести? ')
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            try:
                if amount.isdigit():
                    cur.execute(f"""UPDATE Users_data SET Balance = Balance + {amount} WHERE Number_card = {number_card};""")
                    db.commit()
                    Sql_atm.info_balance(number_card)
                    Sql_atm.report_operation_1(now_date, number_card, '2', amount, '')
                else:
                    print('Попытка выполнить некорректное действие')
            except:
                print('Попытка выполнить некорректное действие')
                return False

    @staticmethod
    def input_operation(number_card):
        """Выбор действия"""
        while True:
            operation = input('Выберите операцию:\n '
                              '1. Узнать баланс\n '
                              '2. Снять денежные средства\n '
                              '3. Внести денежные средства\n '
                              '4. Завершить работу программы\n '
                              '5. Перевести денежные средства\n')
            if operation == '1':
                Sql_atm.info_balance(number_card)
            elif operation == '2':
                Sql_atm.withdrew_money(number_card)
            elif operation == '3':
                Sql_atm.depositing_money(number_card)
            elif operation == '4':
                print('Спасибо!')
                break
            elif operation == '5':
                Sql_atm.transfer_money(number_card)
            else:
                print('Данная операция недоступна')

    @staticmethod
    def transfer_money(number_card):
        """Перевод денежных средств"""
        with sqlite3.connect('atm.db') as db:
            cur = db.cursor()
            try:
                card_for_transfer = input('Введите номер карты для отправки денежных средств: ')
                cur.execute(f"""SELECT Number_card FROM Users_data WHERE Number_card = {card_for_transfer}""")
                result = cur.fetchone()
                result_card = result[0]
                print(result_card)
                if result_card is None or int(result_card) == int(number_card):
                    print('Карты не существует или карта не доступна')
                else:
                    print('Карта найдена')
                    summ_for_transfer = input('Введите сумму для отправки: ')
                    if summ_for_transfer.isdigit() and int(summ_for_transfer) > 0:
                        cur.execute(f"""SELECT Balance FROM Users_data WHERE Number_card = {number_card}""")
                        my_balance = cur.fetchone()
                        result_my_balance = my_balance[0]
                        if result_my_balance - int(summ_for_transfer) > 0:
                            cur.execute(f"""UPDATE Users_data SET Balance = Balance - {summ_for_transfer} WHERE
                                Number_card = {number_card}""")
                            cur.execute(f"""UPDATE Users_data SET Balance = Balance + {summ_for_transfer} WHERE
                                Number_card = {card_for_transfer}""")
                            print('перевод выполнен')
                            Sql_atm.report_operation_1(now_date, number_card, '3', summ_for_transfer,
                                                       card_for_transfer)
                            Sql_atm.report_operation_2(now_date, card_for_transfer, '3', summ_for_transfer,
                                                       number_card)
                        else:
                            print('Недостаточно средств')
                    else:
                        print('Поле должно содержать только цифры и сумму больше 0')
            except:
                print('Данная операция недоступна')

    @staticmethod
    def report_operation_1(now_date, number_card, type_operation, amount, payee):
        """Отчет об операциях № 1"""
        user_data = [(now_date, number_card, type_operation, amount, payee)]
        with open('report_1.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(user_data)
            print('Данные внесены в отчет')

    @staticmethod
    def report_operation_2(date, payee, type_operation, amount, sender):
        """Отчет об операциях № 2"""
        user_data = [(date, payee, type_operation, amount, sender)]
        with open('report_2.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(user_data)
            print('Данные внесены в отчет_2')
