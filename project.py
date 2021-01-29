import json
import requests
import mysql.connector
from environs import Env
from datetime import datetime, timedelta


class ConnectionBD:
    def __init__(self, hos, databs, us, passw, pot):
        self.host = hos
        self.database = databs
        self.user = us
        self.password = passw
        self.port = pot

    def connect_bd(self, client_data):
        """This method connect database and insert data in clientes table."""
        connection = mysql.connector.connect(host=self.host, database=self.database,
                                             user=self.user, password=self.password, port=self.port)
        cpf, nome_completo, nascimento, email, telefone, salario, data_inclusao = client_data
        sql = 'INSERT INTO clientes (cpf, nome_completo, nascimento, email, telefone, salario, proposta_enviada) ' \
              'VALUES (%s, %s, %s, %s, %s, %s, %s)'
        values = (cpf, nome_completo, nascimento, email, telefone, salario, data_inclusao)
        cursor = connection.cursor()
        cursor.execute(sql, values)
        connection.commit()
        print(cursor.rowcount, f'Registro de nome: {nome_completo} foi inserido com sucesso.')
        connection.close()

    def clean_list_offer_bd(self):
        """This method connect database and clean all data of list_ofertas table."""
        connection = mysql.connector.connect(host=self.host, database=self.database,
                                             user=self.user, password=self.password, port=self.port)
        sql = 'TRUNCATE TABLE list_ofertas;'
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        connection.close()

    def fetchall_list_ofertas_bd(self):
        """This method will return all data of lista_ofertas table."""
        connection = mysql.connector.connect(host=self.host, database=self.database,
                                             user=self.user, password=self.password, port=self.port)
        sql = 'SELECT * FROM list_ofertas'
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        return records

    def fetchall_clientes_bd(self, name):
        """This method will return all data of one specific client in cliente table."""
        connection = mysql.connector.connect(host=self.host, database=self.database,
                                             user=self.user, password=self.password, port=self.port)
        sql = f'SELECT * FROM clientes WHERE nome_completo ="{name}"'
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        return records

    def update_clientes_bd(self, name, id_proposal, status_proposal):
        """This method will update database with idproposal and status of one proposal."""
        connection = mysql.connector.connect(host=self.host, database=self.database,
                                             user=self.user, password=self.password, port=self.port)
        sql = f'UPDATE clientes SET idproposta = "{id_proposal}", status_proposta = "{status_proposal}" ' \
              f'WHERE nome_completo = "{name}"'
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        connection.close()

    def insert_list_ofertas_bd(self, api_data):
        """This method connect database and insert offers and date of all offers in list_ofertas table."""
        connection = mysql.connector.connect(host=self.host, database=self.database,
                                             user=self.user, password=self.password, port=self.port)
        for offer in api_data['offers']:
            sql = 'INSERT INTO list_ofertas (ofertas, inclusao) VALUES (%s, %s)'
            code_offer = json.dumps(offer)
            values = (code_offer, datetime.today())
            cursor = connection.cursor()
            cursor.execute(sql, values)
            connection.commit()
        connection.close()


class ConnectionApi(ConnectionBD):
    def __init__(self, hos, databs, us, passw, pot, offer, proposal):
        super().__init__(hos, databs, us, passw, pot)
        self.offer = offer
        self.proposal = proposal

    def api_send_proposal(self, *args):
        """This method receive all data necessary to send proposal of client choosen."""
        proposal_endpoint = self.proposal
        data_information = args[0][1]
        offers_params = args[1][1]
        response_proposal = requests.post(url=proposal_endpoint, data=data_information, json=offers_params)
        result_proposal = response_proposal.json()
        return result_proposal

    def api_receive_offer(self):
        """This method return offer list."""
        offer_endpoint = self.offer
        response = requests.post(url=offer_endpoint)
        result = response.json()
        return result

    def analise_time_api(self, list_record):
        """This method will return list proposal"""
        if not list_record:
            return_api = self.api_receive_offer()
            self.insert_list_ofertas_bd(return_api)
            newrecords = self.fetchall_list_ofertas_bd()
            return newrecords
        else:
            time_offer = list_record[0][2]
            time_api_use = self.time_api(time_offer)
            if time_api_use:
                return list_record
            else:
                return_new_api = self.api_receive_offer()
                self.clean_list_offer_bd()
                self.insert_list_ofertas_bd(return_new_api)
                recordsnew = self.fetchall_list_ofertas_bd()
                return recordsnew

    def analise_time_proposal(self, *args):
        """This method analise proposal and return."""
        for record_information in args[0]:
            situation = self.time_days_api(record_information[2])
            if situation:
                self.connect_bd(args[1])
                return_status_new = self.api_send_proposal(args[1], args[0][-1])
                return f'Nova proposta foi encaminhada com sucesso.' \
                       f'\nProposta nº: {return_status_new["proposal_id"]} - Status: {return_status_new["message"]}'
            else:
                records_clients = self.fetchall_clientes_bd(args[1][1])
                return f'\nO cliente já encaminhou uma proposta a menos de 30 dias, segue os dados da ultima ' \
                       f'proposta do cliente:\nid_proposal: {records_clients[-1][8]}\nstatus: {records_clients[-1][9]}'

    def final_process(self, list_client_offer, client_user):
        """This method will inform if the client has offer or if the proposal was sent correctly."""
        if list_client_offer:
            records_clients = self.fetchall_clientes_bd(client_user[1])
            if not records_clients:
                self.connect_bd(client_user)
                return_status = self.api_send_proposal(client_user, list_client_offer[-1])
                self.update_clientes_bd(client_user[1], return_status["proposal_id"], return_status["message"])
                return f'Proposta nº: {return_status["proposal_id"]} - Status: {return_status["message"]}'
            else:
                return_analise = self.analise_time_proposal(list_client_offer, client_user)
                return return_analise
        else:
            return 'O cliente informado não possui oferta válida.'

    def register_user(self):
        """This method register user data."""
        cpf = input('Numero do CPF do cliente (somente numeros):')
        usuario = input('Nome do cliente:')
        birth = input('Data de nascimento do cliente (ex. 12/01/2001):')
        email = input('Email do cliente:')
        cell = input('Telefone do cliente (ex. 21942365978):')
        salary = float(input('Salário do cliente:'))
        incl = datetime.today()
        return cpf, usuario, self.formatdates(birth), email, cell, salary, incl,

    @staticmethod
    def formatdates(birth_date):
        """This method format birth_date.Ex: d/m/y to y-m-d"""
        formatdata = datetime.strptime(birth_date, '%d/%m/%Y').date()
        return str(formatdata)

    @staticmethod
    def offer_client(*args):
        """This method select offers to one user."""
        allinfo = []
        for data in args[0]:
            individual_offer = json.loads(data[1])
            if args[1][1] == individual_offer['partner_name']:
                allinfo.append(data)
        return allinfo

    @staticmethod
    def time_api(time_record):
        """This method will calcule time of last request, if the time is minor 10 minutes the return will be True."""
        time_now = datetime.today()
        dif = time_now - time_record
        if dif < timedelta(minutes=10):
            return True
        else:
            return False

    @staticmethod
    def time_days_api(time_record):
        """This method will calcule time of last proposal, if the time is minor 30 days the return will be False."""
        time_now = datetime.today()
        dif = time_now - time_record
        if dif > timedelta(days=30):
            return True
        else:
            return False


if __name__ == "__main__":
    # Set environment variable
    env = Env()
    env.read_env()
    secret_offer_endpoint = env.str('NT_offer_endpoint')
    secret_proposal_endpoint = env.str('NT_proposal_endpoint')
    host = env.str('NT_BD_HOST')
    database = env.str('NT_BD_DATABASE')
    user = env.str('NT_BD_USER')
    password = env.str('NT_BD_PASSWORD')
    port = env.int('NT_BD_PORT')

    # Creating instance with class ConnectionBD
    connectbd = ConnectionBD(host, database, user, password, port)
    # Creating instance with class ConnectionApi
    connectapi = ConnectionApi(host, database, user, password, port, secret_offer_endpoint, secret_proposal_endpoint)
    # Extract all information in database list_ofertas
    records_list_offertas = connectbd.fetchall_list_ofertas_bd()
    # Analyse the time of last request
    data_offer = connectapi.analise_time_api(records_list_offertas)
    # Insert all data each client
    inform_client = connectapi.register_user()
    # Analyse if the client has valid offer
    client_offer = connectapi.offer_client(data_offer, inform_client)
    # Finish the process in database
    return_process = connectapi.final_process(client_offer, inform_client)
    print(return_process)
