import psycopg2
import numpy as np
import datetime


def generate_number():
    latin_letters = ['A', 'B', 'C', 'E', 'H', 'K', 'M', 'O', 'P', 'T', 'X', 'Y']
    all_numbers = [int(i) for i in range(0, 10)]
    int_number = np.random.choice(all_numbers, 3)
    region = np.random.choice(all_numbers, 2)
    letters = np.random.choice(latin_letters, 3)


    final_number = letters[0] + letters[1] + str(int_number[0]) + \
                    str(int_number[1]) + str(int_number[2]) + letters[2] + \
                    str(region[0]) + str(region[1])

    return final_number


# generate autopark
def generate_autopark(cursor, size):
    cursor.execute(""" select "Brand", "Model" from "Cars" """)
    cars = cursor.fetchall()

    for _ in range(0, size):
        number = generate_number()
        car_ind = np.random.randint(len(cars), size=1)[0]
        car = cars[car_ind]
        cursor.execute(""" insert into "Auto_park" values (%s, %s , %s, True) """,
                        (car[0], car[1], number))


def generate_name():
    names = ['Максим', 'Александр', 'Михаил', 'Иван', 'Дмитрий', 'Даниил', 'Кирилл', 'Егор', 'Илья', 'Матвей']


    midnames = ['Данилович', 'Денисович', 'Дмитриевич', 'Евгеньевич',
                'Егорович', 'Ефимович', 'Иванович', 'Игнатьевич', 'Игоревич',
                'Ильич', 'Иосифович', 'Исаакович']

    surnames = [ 'Абрамов', 'Авдеев', 'Агафонов', 'Аксёнов', 'Александров',
                'Алексеев', 'Андреев', 'Анисимов', 'Антонов', 'Артемьев',
                'Гусев', 'Гущин', 'Давыдов', 'Данилов','Дементьев','Денисов',
                'Дмитриев', 'Доронин', 'Дорофеев', 'Дроздов', 'Дьячков',
                'Евдокимов', 'Евсеев', 'Егоров', 'Костин', 'Котов', 'Кошелев',
                'Красильников', 'Крылов', 'Крюков', 'Кудрявцев', 'Кудряшов',
                'Кузнецов', 'Кузьмин', 'Кулагин']



    name_ind = np.random.randint(len(names), size=1)[0]
    midname_ind = np.random.randint(len(midnames), size=1)[0]
    surname_ind = np.random.randint(len(surnames), size=1)[0]

    #surname = ' '.join(surnames[surname_ind]).decode('utf-8')

    return str(surnames[surname_ind]), str(names[name_ind]), str(midnames[midname_ind])


def generate_birthdate():
    year = np.random.randint(1950, 2000, 1)[0]
    day = np.random.randint(1, 28, 1)[0]
    month = np.random.randint(1, 12, 1)[0]

    date = datetime.date(year, month, day)

    return date


def generate_city(cursor):
    cursor.execute(""" select "city" from "cities" """)
    cities =  cursor.fetchall()

    city_ind = np.random.randint(len(cities), size=1)[0]
    return cities[city_ind]


# generate clients
def generate_clients(cursor, size):

    for _ in range(0, size, 1):
        surname, name, midname = generate_name()
        passport_number = str(np.random.randint(1000000000, 9999999999, 1)[0])
        driving_number = str(np.random.randint(1000000000, 9999999999, 1)[0])
        date = str(generate_birthdate())
        city = generate_city(cursor)

        cursor.execute("""insert into "Clients" values (%s, %s, %s, %s, %s, %s, %s)""",
                        [passport_number, driving_number, surname, name, midname, date, city])


def generate_order_date():
    year = np.random.randint(2010, 2018, 1)[0]
    day = np.random.randint(1, 28, 1)[0]
    month = np.random.randint(1, 13, 1)[0]

    date = datetime.date(year, month, day)

    return date


# generate history
def generate_history(cursor, size):
    cursor.execute(""" select "auto_number" from "Auto_park" """)
    auto_numbers = cursor.fetchall()

    cursor.execute(""" select "passport_num", "driving_licence" from "Clients" """)
    clients_data = cursor.fetchall()

    order_nums = []

    for _ in range(0, size):

        order_date = generate_order_date()
        order_cost = str(np.random.randint(300, 20000, 1)[0])

        auto_number_ind = np.random.randint(len(auto_numbers), size=1)[0]
        driving_and_passport_ind = np.random.randint(len(clients_data), size=1)[0]

        auto_number = auto_numbers[auto_number_ind]
        driving_and_passport = clients_data[driving_and_passport_ind]

        passport_num = driving_and_passport[0]
        driving_licence = driving_and_passport[1]

        order_num = str(np.random.randint(10000, 900000, size=1)[0])

        while order_num in order_nums:
            order_num = str(np.random.randint(10000, 900000, size=1)[0])

        order_nums.append(order_num)

        cursor.execute("""insert into "history" values (%s, %s, %s, %s, %s, %s)""",
                    [order_num, auto_number, driving_licence, order_date, order_cost, passport_num])


#def create_users(cursor):


def get_connection():
    conn = psycopg2.connect("dbname='CarSharing' user='pavelapalkov' host='localhost' password='connpass'")
    return conn


def close_connection(connection):
    connection.close()


def main():
    connection = get_connection()

    #generate_autopark(connection.cursor(), 500)
    #generate_clients(connection.cursor(), 300)
    generate_history(connection.cursor(), 3000)

    connection.commit()

    close_connection(connection)


if __name__ == '__main__':
    main()
