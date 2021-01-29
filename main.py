import project as cb


# TODO 1 - CRIAR OS BANCOS DE DADOS COM AS TABELAS CLIENTES E LIST_OFERTAS



conbd = cb.ConnectionBD('localhost', 'test_clients', 'root', 'A&?UDgQt43Tk', 3306)
conapi = cb.ConnectionApi('localhost', 'test_clients', 'root', 'A&?UDgQt43Tk', 3306)

records_list_offertas = conbd.fetchall_list_ofertas_bd()
data_offer = conapi.analise_time_api(records_list_offertas)

inform_client = conapi.register_user()

client_offer = conapi.offer_client(data_offer, inform_client)

return_process = conapi.final_process(client_offer, inform_client)
print(return_process)
