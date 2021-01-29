# repositorio_creditofacil
Este repositório tem como finalidade hospedar o projeto de teste técnico desenvolvido em python para uma empresa de analise de crédito renomada no mercado brasileiro. 

Ambiente de desenvolvimento
Linguagem : Python 3.8;
IDE : Pycharm;
Bibliotecas : requests, Mysql.connector, Datetime, timedelta, environs e json.
Banco de Dados: Mysql.

Preparação do ambiente
Orientações iniciais que deverão ser adotados para que a solução funcione corretamente.
Passo 1 - Copiar o arquivo "project.py" para uma pasta que será usada pelo editor de texto de sua preferencia.
Passo 2 - Instalar a biblioteca "environs" por meio do terminal do seu editor de texto. Ex: pip install environs
Passo 3 - Instalar a biblioteca "mysql-connector" por meio do terminal do seu editor de texto. ex: pip install mysql-connector
Passo 4 - Preencher os dados solicitados no arquivo nomeado "modelo_env.txt", o referido arquivo é um modelo que foi utilizado como variável de ambiente.
Passo 5 - Criar um arquivo ".env", dentro da mesma pasta que esta o arquivo "project.py", que deverá conter todos os dados preenchidos no arquivo "modelo_env.txt".  

Desafio

2.1 – O marketplace
Vamos supor que existem dois fluxos somente na criação do nosso marketplace, o de
exibir ofertas e o de enviar proposta para a empresa parceira. Com isso, precisamos
que sejam criados dois endpoints para que possamos realizar estes fluxos. Abaixo
explicaremos cada endpoint.
Neste desafio você precisará utilizar as entidades de Cliente e Oferta listadas no item
2.1.3.
Observe com carinho o item 2.1.4, nele tem alguns plus que você pode ousar em fazer
e ficaremos ainda mais felizes.
2.1.1 – Endpoint de exibir Oferta
Este endpoint retorna ofertas.
Como entrada do serviço, necessitamos das informações do cliente para buscar as
ofertas do mesmo.
As ofertas estarão em um endpoint informado no email e têm validade de 10 min,
então dentro deste tempo não precisamos fazer uma nova requisição para este
endpoint.
O retorno deste endpoint será uma lista de ofertas.
2.1.2 – Endpoint de envio de Proposta
Este endpoint envia uma proposta.
Como entrada deste serviço, necessitamos das informações do cliente e da oferta
escolhida pelo mesmo.
O envio da proposta será por um endpoint que também estará informado no email.
Com isso temos a necessidade de validar se o cliente já enviou a mesma proposta nos
últimos 30 dias. Caso ele tenha enviado, precisamos retornar uma mensagem para o
cliente informando que o mesmo já enviou uma proposta para esta oferta. Caso ele
não tenha enviado, precisamos salvar essa proposta para um envio posterior e enviála.
O retorno deste endpoint será um id da proposta e uma mensagem.
Obs.: Uma proposta é composta pelos dados do cliente e da oferta.
