from sql_query import Sql_atm


class Atm:

    Sql_atm.create_table()
    Sql_atm.insert_user((1234, 1111, 10000))
    Sql_atm.insert_user((2345, 2222, 10000))
    number_card = input('Введите пожалуйста номер карты: ')
    while True:
        if Sql_atm.input_card(number_card):
            if Sql_atm.input_code(number_card):
                Sql_atm.input_operation(number_card)
                break
            else:
                break
        else:
            break
