import psycopg2
from flask import Flask, request, g, redirect, url_for, render_template, session, send_file
import datetime
from docxtpl import DocxTemplate
import xlsxwriter
import numpy as np
import pandas as pd
from os import system


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my key'

cars_connection = conn = psycopg2.connect("dbname='CarSharing' port=5432 user='pavelapalkov' host='localhost' password='connpass'")
users_connection = conn = psycopg2.connect("dbname='CarSharing' port=5433 user='pavelapalkov' host='localhost' password='connpass'")

#master_connection = conn = psycopg2.connect("dbname='CarSharing' port=5432 user='pavelapalkov' host='localhost' password='connpass'")
#slave_connection = conn = psycopg2.connect("dbname='CarSharing' port=5433 user='pavelapalkov' host='localhost' password='connpass'")


def connect_conn():
    conn = psycopg2.connect("dbname='CarSharing' user='pavelapalkov' host='localhost' password='connpass'")
    return conn


def get_conn():
    if not hasattr(g, 'psql'):
        g.psql = connect_conn()
    return g.psql


@app.teardown_appcontext
def close_conn(error):
    if hasattr(g, 'psql'):
        g.psql.close()


@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/')
def start_page():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return home()


@app.route('/home')
def home():
    print(session["username"])
    return render_template('client/home.html', username = session["username"])


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    #cursor = get_conn().cursor()
    cursor = users_connection.cursor()

    #cursor = slave_connection.cursor()

    cursor.execute(""" select "password" from "users" where "username"=%s """, [username])
    result = cursor.fetchall()
    print(len(result))
    if len(result) != 0:
        result = result[0][0]
    else:
        return start_page()

    print(result)
    if result == password:
        session['logged_in'] = True
        session['username'] = username

    return start_page()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return start_page()

@app.route('/add_clients_form')
def add_clients_form():
    return render_template('client/add_clients.html')


@app.route('/add_clients', methods=['POST'])
def add_clients():
    conn = get_conn()

    conn.cursor().execute("""insert into "Clients" values (%s, %s, %s, %s, %s, %s, %s)""",
                [request.form['passport'], request.form['driving_l'],
                 request.form['surname'],request.form['name'],
                 request.form['midname'],request.form['birthdate'], request.form['city']])


    conn.cursor().execute("""insert into "users" values (%s, %s, %s)""",
                [request.form['username'], request.form['password'],
                 request.form['passport']])

    conn.commit()

    session['logged_in'] = True
    session['username'] = request.form['username']

    return redirect(url_for('start_page'))



@app.route('/admin/clients_statistics')
def clients_statistics():
    cursor = get_conn().cursor()
    cursor.execute(""" select "birth_date" from "Clients" """)
    all_birthdates = cursor.fetchall()

    today = datetime.date.today()
    ages = [int((today - birthdate[0]).days / 365) for birthdate in all_birthdates]


    ages_groups = []
    age_18_21 = 0
    age_22_30 = 0
    age_31_40 = 0
    age_41_50 = 0
    age_51_60 = 0
    age_61_more = 0

    for age in ages:
        if (age > 18) and (age <= 21):
            age_18_21 += 1

        elif (age > 21) and (age <= 30):
            age_22_30 += 1

        elif (age > 30) and (age <= 40):
            age_31_40 += 1

        elif (age > 40) and (age <= 50):
            age_41_50 += 1

        elif (age > 50) and (age <= 60):
            age_51_60 += 1

        elif (age > 60):
            age_61_more += 1


    ages_groups.append(["18-21", age_18_21])
    ages_groups.append(["22-30", age_22_30])
    ages_groups.append(["30-40", age_31_40])
    ages_groups.append(["40-50", age_41_50])
    ages_groups.append(["50-60", age_51_60])
    ages_groups.append([">60", age_61_more])


    cursor.execute("""select * from "Clients" """)
    clients_data = cursor.fetchall()

    dict_clients_data = []
    for client in clients_data:
        dict_data = {}
        dict_data['Passport'] = client[0]
        dict_data['Driving'] = client[1]
        dict_data['Surname'] = client[2]
        dict_data['Name'] = client[3]
        dict_data['Midname'] = client[4]
        dict_data['Birth date'] = str(client[5])
        dict_data['City'] = client[6]

        dict_clients_data.append(dict_data)

    cursor.execute("""select "username", "passport_number" from "users" """)
    users = cursor.fetchall()

    users_list = []

    for user in users:

        user_dict = {}
        user_dict['value'] = user[0]
        cursor.execute("""select * from "Clients" where "passport_num"=%s """, [user[1]])
        client = cursor.fetchall()[0]
        dict_data = {}
        dict_data['Passport'] = client[0]
        dict_data['Driving'] = client[1]
        dict_data['Surname'] = client[2]
        dict_data['Name'] = client[3]
        dict_data['Midname'] = client[4]
        dict_data['Birthdate'] = str(client[5])
        dict_data['City'] = client[6]

        user_dict['data'] = dict_data
        users_list.append(user_dict)


    return render_template('admin/clients_statistics.html', ages_groups=ages_groups,
                            clients_data=dict_clients_data, users_info=users_list)

@app.route('/export_client_info', methods=['POST'])
def export_client_info():
    cursor = get_conn().cursor()


    username = request.form["login"]

    cursor.execute("""select "passport_number" from "users" where "username"=%s """, [username])

    passport = cursor.fetchall()[0]
    cursor.execute("""select * from "Clients" where "passport_num"=%s """, [passport])

    client = cursor.fetchall()[0]

    dict_data = {}
    dict_data['passport'] = client[0]
    dict_data['driving'] = client[1]
    dict_data['surname'] = client[2]
    dict_data['name'] = client[3]
    dict_data['midname'] = client[4]
    dict_data['bdate'] = str(client[5])
    dict_data['city'] = client[6]

    doc = DocxTemplate("saves/templates/template.docx")
    doc.render(dict_data)
    doc.save("saves/client_card.docx")

    try:
        system("open saves/client_card.docx")
        return send_file("saves/client_card.docx", attachment_filename="client_card.docx")
    except Exception as e:
        return str(e)


@app.route('/admin/export_clients_csv')
def export_clients_csv():
    cursor = get_conn().cursor()

    cursor.execute("""select * from "Clients" """)

    clients_data = cursor.fetchall()

    clients_data = pd.DataFrame(clients_data, columns=["Фамилия", "Имя", "Отчество", "Дата рождения",
                                                        "Паспорт", "ВУ", "Город"])

    clients_data.to_csv("saves/clients.csv")

    try:
        #system("open saves/clients.csv")
        return send_file("saves/clients.csv", attachment_filename="clients.csv")
    except Exception as e:
     return str(e)


@app.route('/admin/export_clients_excel')
def export_clients_excel():
    cursor = get_conn().cursor()

    cursor.execute("""select * from "Clients" """)

    clients_data = cursor.fetchall()
    clients_data = np.array(clients_data)


    workbook = xlsxwriter.Workbook('saves/clients.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.set_column(0, 10, 15)
    row = 3
    col = 0

    for passport, driving, surname, name, midname, bdate, city in (clients_data):
        worksheet.write_string(row, col, surname)
        worksheet.write_string(row, col+1, name)
        worksheet.write_string(row, col+2, midname)
        worksheet.write_string(row, col+3, str(bdate))
        worksheet.write_string(row, col + 4, passport)
        worksheet.write_string(row, col + 5, driving)
        worksheet.write_string(row, col + 6, city)
        row += 1

    bold = workbook.add_format({'bold': True})

    worksheet.write('A4', 'Фамилия', bold)
    worksheet.write('B4', 'Имя', bold)
    worksheet.write('C4', 'Отчество', bold)
    worksheet.write('D4', 'Дата рождения', bold)
    worksheet.write('E4', 'Паспорт', bold)
    worksheet.write('F4', 'ВУ', bold)
    worksheet.write('G4', 'Город', bold)

    worksheet.write('A1', 'Всего клиентов:', bold)
    worksheet.write_string(0, 1, str(len(clients_data)))

    workbook.close()

    try:
        system("open saves/clients.xlsx")
        return send_file("saves/clients.xlsx", attachment_filename="clients.xlsx")
    except Exception as e:
     return str(e)



@app.route('/admin/auto_park_statistics')
def auto_park_statistics():
    #cursor = get_conn().cursor()
    cursor = cars_connection.cursor()

    #cursor = master_connection.cursor()
    cursor.execute(""" select "Brand" from "Cars" """)
    all_cars = cursor.fetchall()

    cars_num = []
    for car in all_cars:
        cursor.execute(""" select count("Brand") from "Auto_park" where "Brand"=%s""", [car])
        car_num = cursor.fetchall()[0][0]
        cars_num.append([car[0], car_num])

    cursor.execute("""select * from "Auto_park" """)
    cars_data = cursor.fetchall()

    dict_cars_data = []
    for car in cars_data:
        dict_data = {}
        dict_data['Brand'] = car[0]
        dict_data['Model'] = car[1]
        dict_data['Number'] = car[2]
        dict_data['Free'] = "Свободно" if car[3] is True else "Занято"

        dict_cars_data.append(dict_data)

    return render_template('admin/auto_park_statistics.html', cars_num=cars_num, cars_data=dict_cars_data)


@app.route('/admin/cars_statistics')
def cars_statistics():
    cursor = get_conn().cursor()
    cursor.execute("""select * from "Cars" """)
    cars_data = cursor.fetchall()

    dict_cars_data = []
    for car in cars_data:
        dict_data = {}
        dict_data['Brand'] = car[0]
        dict_data['Model'] = car[1]
        dict_data['Passengers Max.'] = car[2]
        dict_data['Power'] = car[3]
        dict_data['Drive'] = "Передний" if car[4] is True else "Задний"
        dict_data['Hour price'] = car[5]
        dict_data['Day price'] = car[6]
        dict_data['Night price'] = car[7]
        dict_data['Full day price'] = car[8]

        dict_cars_data.append(dict_data)

    return render_template('admin/cars_statistics.html', cars_data=dict_cars_data)


@app.route('/admin/orders')
def orders():
    cursor = get_conn().cursor()
    cursor.execute("""select * from "orders" """)
    orders_data = cursor.fetchall()

    dict_orders_data = []
    for order in orders_data:
        dict_data = {}
        dict_data['Number'] = order[0]
        dict_data['Brand'] = order[1]
        dict_data['Model'] = order[2]
        dict_data['Beginnig'] = str(order[3])
        dict_data['Ending'] = str(order[4])
        dict_data['Confirmed'] = "Да" if order[5] is True else "Нет"
        dict_data['Taken'] = "Да" if order[6] is True else "Нет"
        dict_data['Driving'] = order[7]

        dict_orders_data.append(dict_data)

    return render_template('admin/orders.html', orders_data=dict_orders_data)



@app.route('/admin/history_statistics')
def history_statistics():
    cursor = get_conn().cursor()
    cursor.execute(""" select "order_date" from "history" """)
    all_dates = cursor.fetchall()


    all_years =[#['date', 'Январь' , 'Февраль' , 'Март' , 'Апрель' , 'Май' ,
                #        'Июнь' , 'Июль' , 'Август' , 'Сентябрь' , 'Октябрь' , 'Ноябрь' , 'Декабрь'],
                ['2010', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                ['2011', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                ['2012', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                ['2013', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                ['2014', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                ['2015', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                ['2016', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                ['2017', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    for date in all_dates:
        year = int(str(date[0])[3])
        single_month = int(str(date[0])[5:7])
        all_years[year][single_month] += 1

    cursor.execute("""select * from "history" """)
    history_data = cursor.fetchall()

    dict_history_data = []
    for record in history_data:
        dict_data = {}
        dict_data['Number'] = record[0]
        dict_data['Auto number'] = record[1]
        dict_data['Driving'] = record[2]
        dict_data['Date'] = str(record[3])
        dict_data['Cost'] = record[4]
        dict_data['Passport'] = record[5]

        dict_history_data.append(dict_data)

    return render_template('admin/history_statistics.html', all_years=all_years[-2:], hist_data=dict_history_data)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
