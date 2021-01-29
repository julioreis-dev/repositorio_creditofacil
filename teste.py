from time import time, sleep
from datetime import datetime, timedelta
import mysql.connector

# x = datetime.today()
# sleep(5)
# y= datetime.today()
# dif = y - x
# print(dif)
# if dif < timedelta(minutes=1):
#     print('Aplicação não usa a API')
#
# a = [18]
# print(a[-1])
def create_database():
    connection = mysql.connector.connect(host='localhost', user='root', password='A&?UDgQt43Tk')

    mycursor = connection.cursor()
    mycursor.execute("CREATE DATABASE test_clients")

def create_client_table():
    connection = mysql.connector.connect(host='localhost', database='test_clients',
                                                 user='root', password='A&?UDgQt43Tk', port=3306)
    cursor = connection.cursor()
    sql = """CREATE TABLE IF NOT EXISTS clientes (
       idclientes INT NOT NULL AUTO_INCREMENT,
       cpf VARCHAR(11) NOT NULL,
       nome_completo VARCHAR(100) NOT NULL,
       nascimento VARCHAR(10) NOT NULL,
       email VARCHAR(100) NOT NULL,
       telefone VARCHAR(11) NOT NULL,
       salario FLOAT NOT NULL,
       proposta_enviada DATETIME NULL,
       idproposta INT NULL,
       status_proposta VARCHAR(30) NULL,
       PRIMARY KEY (idclientes))"""
    cursor.execute(sql)
    connection.close()

def create_list_offer_table():
    connection = mysql.connector.connect(host='localhost', database='test_clients', user='root',
                                         password='A&?UDgQt43Tk', port=3306)
    cursor = connection.cursor()
    sql = """CREATE TABLE IF NOT EXISTS list_ofertas (
            idofertas INT NOT NULL AUTO_INCREMENT,
            ofertas JSON NULL,
            inclusao DATETIME NULL,
            PRIMARY KEY (idofertas))"""
    cursor.execute(sql)
    connection.close()

create_database()
create_client_table()
create_list_offer_table()
