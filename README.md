# repositorio_creditofacil
Este repositório tem como finalidade hospedar o projeto de teste técnico desenvolvido em python para uma empresa de analise de crédito renomada no mercado brasileiro. 

Ambiente de desenvolvimento:

Linguagem : Python 3.8;
IDE : Pycharm;
Bibliotecas : requests, Mysql.connector, Datetime, timedelta, environs e json.
Banco de Dados: Mysql.

Orientações iniciais:

Passo 1 - Copiar o arquivo "project.py" e "project_bd.py para a pasta que será usada pelo editor de texto de sua preferencia.
Passo 2 - Ler a documentação do arquivo "project.py" que orienta os passos finais para o funcionamento da aplicação.

Desafio:

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

Solução:

O projeto desenvolvido atendeu a todos os requisitos solicitados no escopo do desafio. Diante da necessidade de proteger o fluxo de dados foi necesário desenvolver todo o projeto tendo como necessidade a criação de variavel de ambiente afim de proteger os endpoints utilizados e as variaveis necessárias para a conexão com o bando de dados.
A aplicação inicialmente consome a API referente ao fluxo de ofertas e inseri no BD, durante 10 minutos todo o cadastro de um cliente terá os seus dados checados por meio dos dados presentes no BD, neste momento a API deixa de ser usada e somente apos esse período a aplicação renova os dados fazendo com que todo o conteúdo seja excluído e seja realizado uma nova chamada da API e iserindo os dados no BD.
A inclusão de um cliente no BD somente ocorrerá se o mesmo tiver uma oferta válida, caso exista, todos os dados serão incluídos juntamente com o id da proposta e o status da proposta, dados estes que fazem parte do retorno da API de envio da proposta. Tal registros se faz necessário para caso seja feito um novo registro do cliente, possa se verificar por meio do id da proposta se a ultimma proposta válida encontra-se dentro do período de 30 dias com foi solicitado no desafio. Se a ultima proposta válida tiver sido encaminhada com o prazo menor do que 30 dias a aplicação irá mostra um protocolo comprovanto que o cliente já possui oferta válida e cadastrada.
Caso se tente cadastrar um cliente que não possui oferta válida a aplicação informará que o cliente não possui oferta válida.
