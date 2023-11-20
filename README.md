# Sistema de mensageria distribuído para web em tempo real

## Índice

1. [Resumo](#1-resumo)
2. [Introdução](#2-introdução)
3. [Desenvolvimento](#3-desenvolvimento)
   1. [Aplicações web e microsserviços](#31-aplicações-web-e-microsserviços)
   2. [Escalabilidade horizontal e aplicações em tempo real](#32-escalabilidade-horizontal-e-aplicações-em-tempo-real)
   3. [Solução proposta](#33-solução-proposta)
   4. [Protocolo de consenso](#34-protocolo-de-consenso)
   5. [Implementação](#35-implementação)
   6. [Comparação entre sistemas de mensageria](#36-comparação-entre-sistemas-de-mensageria)

## 1. Resumo

Este trabalho tem como objetivo apresentar o desenvolvimento de uma aplicação de mensageria distribuída como uma abordagem para problemas de escalabilidade para aplicações web que se utilizem de recursos em tempo real, em especial para casos onde existe a comunicação entre cliente-servidor.
A aplicação foi desenvolvida utilizando a linguagem de programação Go e disponibiliza um cliente em Javascript/Typescript para ser utilizado em aplicações web.

## 2. Introdução

Aplicações web com interação em tempo real são cada vez mais comuns, seja para fins de comunicação entre usuários, seja para fins de monitoramento de dados em tempo real. Uma grande quantidade de aplicações são desenvolvidas com interatividade e experiência do usuário em mente, e a comunicação em tempo real é um dos recursos que mais contribuem para isso. Redes sociais são um exemplo de aplicações que utilizam recursos em tempo real, elas comumente implementam recursos em tempo real para notificações de novas mensagens, curtidas ou comentários. Essas interações enriquecem a experiência do usuário, não necessitando de recarregamento ou ações manuais para para que as novas informações sejam exibidas.
Tendo isso em mente, o objetivo desse trabalho é apresentar uma aplicação alternativa para elaboração de aplicações web com recursos em tempo real, simplificando a implementação de tais recursos no lado do cliente e do servidor. Além da aplicação, serão apresentados os resultados de testes de desempenho e escalabilidade, comparando a aplicação desenvolvida com modelos de arquitetura padrões para esse tipo de problema.

## 3. Desenvolvimento

Este trabalho origina-se das necessidades das aplicações web atuais, onde cada vez são adicionadas mais funcionalidades no lado do cliente para que a experiência do usuário seja a melhor possível. Com isso, a complexidade das aplicações aumenta, e a necessidade de uma comunicação em tempo real entre cliente e servidor se torna cada vez mais comum. A comunicação em tempo real entre cliente e servidor é um problema que pode ser resolvido de diversas formas, e cada uma delas possui suas vantagens e desvantagens. A aplicação desenvolvida neste trabalho tem como objetivo simplificar a implementação de recursos em tempo real no lado do cliente e do servidor, além de ser uma alternativa para problemas de escalabilidade.

## 3.1 Aplicações web e microsserviços

Originalmente, aplicações web tradicionais eram monolíticas, isto é, necessitavam de uma única máquina para serem executadas. Com o crescimento da web e a disponibilização de vários serviços com milhares de usuários através dela, a quantidade de processamento necessária para atender a demanda de usuários cresceu exponencialmente. Com isso, a necessidade de escalabilidade também cresceu, e a arquitetura de aplicações web evoluiu para um modelo distribuído, onde a aplicação é executada em várias máquinas, e cada uma delas é responsável por uma parte da aplicação. Esse modelo de arquitetura é conhecido como arquitetura de microsserviços.

Arquiteturas de microsserviços consistem na divisão de uma aplicação em diversos serviços menores, cada um com sua própria responsabilidade. Isso permite que a aplicação seja dividida em pequenos módulos, cada um com seu domínio especializado e seus recursos computacionais. Essa abordagem possibilita que cada serviço seja escalado individualmente, de acordo com a demanda de cada um. Além disso, a divisão da aplicação em serviços menores permite que cada serviço seja desenvolvido utilizando a linguagem de programação mais adequada para o problema que ele resolve, e que cada serviço seja executado em uma máquina diferente. Isso permite que a aplicação seja escalada horizontalmente, isto é, que ela seja executada em várias máquinas diferentes, cada uma responsável por um serviço diferente. Essa abordagem é conhecida como escalabilidade horizontal.

## 3.2 Escalabilidade horizontal e aplicações em tempo real

A escalabilidade horizontal vem com seus próprios desafios, em especial para aplicações que necessitam de estado. Aplicações web tradicionais, que utilizam o modelo de arquitetura monolítica, possibilitam o armazenamento de estado, uma vez que executam em um único servidor, entretanto a escalabilidade desse tipo de aplicação é limitada e custosa, pois necessita de acréscimo de hardware para aumentar seu poder computacional.

Para aplicações distribuídas, a escalabilidade horizontal facilita o aumento de poder computacional, sendo necessário apenas adicionar mais servidores em um _cluster_. Porém, esse tipo de escalabilidade apresenta um desafio para servidores que necessitam manter conexão com o cliente, como é o caso das aplicações web em tempo real. Nesses casos, é comum ver arquiteturas como na da imagem abaixo.

![Sistema distribuído com mensageria](architectures/rt-messaging.png)

Nesse tipo de arquitetura, utiliza-se um serviço de mensageria para notificar servidores de atualização de estado, para que ele possa distribuir isso para outras máquinas conectadas em um cluster. Essa é uma das estratégias que serviços que se utilizam de atualizações em tempo real implementam.

Essa é uma abordagem válida, porém adiciona complexidade na implementação do sistema, como gerenciamento da infraestrutura do serviço de mensageria e a implementação da lógica de distribuição de mensagens no servidor de comunicação, além do gerenciamento de clientes conectados nos servidores.

## 3.3 Solução proposta

O intuito da aplicação desenvolvida nesse trabalho é simplificar a complexidade da arquitetura necessária para desenvolver aplicações em tempo real para a web. Adicionando um único serviço de mensageria, responsável por receber as atualizações da aplicação e distribuí-la entre os clientes conectados.

![Sistema distribuído](architectures/repl.png)

A distribuição das mensagens é feita através de tópicos, onde cada tópico é responsável por um tipo de mensagem. Os clientes podem se inscrever em um ou mais tópicos, e o serviço de mensageria distribuí as mensagens para os clientes inscritos em cada tópico. Essa abordagem simplifica a implementação de serviços em tempo real, uma vez que para notificar clientes conectados de uma atualização, é necessário somente a publicação de uma mensagem para um tópico.

```mermaid
sequenceDiagram
  participant Cliente
  participant Mensageria

  Cliente->>Mensageria: Inscreve-se em um tópico X
  Mensageria->>Cliente: Confirma inscrição
  loop Atualizações do tópico
    Mensageria->>Cliente: Envia atualizações do tópico X
  end
```

Nesse modelo, para que o cliente receba atualizações de um tópico, ele precisa se inscrever no tópico desejado. Após a inscrição, o cliente passa a receber atualizações do tópico, e pode se inscrever em outros tópicos, podendo receber atualizações de vários tópicos ao mesmo tempo.

Para a aplicação, os clientes se conectam através do padrão _Server-Sent-Events_ (Eventos enviados pelo servidor), um padrão de comunicação unidirecional baseado em mensagens enviadas pelo servidor através do protocolo HTTP.

```mermaid
sequenceDiagram;
  participant Cliente
  participant Servidor

  Cliente->>Servidor: Requisição de conexão
  Servidor->>Cliente: Conexão estabelecida
  loop
    Servidor->>Cliente: Envia atualizações de estado
  end
  Cliente->>Servidor: Desconecta da conexão
```

Essa tecnologia possibilita que o servidor envie mensagens para o cliente através de uma conexão HTTP, sem que o cliente precise fazer requisições ativamente para o servidor. O cliente pode se conectar ao servidor através de um endpoint específico, e o servidor pode enviar mensagens para o cliente através de um outro endpoint específico. O cliente pode se desconectar do servidor a qualquer momento, e o servidor pode enviar mensagens para o cliente enquanto a conexão estiver estabelecida.

A principal vantagem do SSE em relação a alternativas como WebSocket é a simplicidade da implementação e velocidade de desenvolvimento. O SSE é uma tecnologia nativa do protocolo HTTP, e não necessita de bibliotecas externas para ser implementado. Além disso, o SSE é um protocolo unidirecional, o que simplifica a implementação do servidor, uma vez que ele não precisa gerenciar requisições do cliente.

## 3.4 Protocolo de consenso

O sistema funciona em modo de nó único e em cluster. Em modo de nó único, o sistema executa em uma única máquina, e não é possível adicionar mais nós. Em modo de cluster, o sistema executa em várias máquinas, e é possível adicionar mais nós ao cluster. O sistema utiliza o protocolo Raft para consenso entre os nós do cluster, para garantir consistência entre os nós e a entrega da mensagem para os tópicos entre cada máquina do cluster. Inicialmente os nós contam com um "bootstrap" para que o cluster seja inicializado, esse nó é responsável por iniciar o cluster e adicionar novos nós ao cluster.

O processo de replicação no Raft inicia com a eleição de um líder, que é responsável por coordenar e distribuir as operações para os demais servidores seguidores. O líder recebe comandos dos clientes, adiciona esses comandos ao seu log e replica esses logs para os seguidores. Os seguidores, por sua vez, aplicam esses comandos aos seus estados, mantendo assim a consistência entre os diferentes servidores no cluster.

O Raft lida eficientemente com situações de falha, como a queda de um líder, ao realizar eleições de forma determinística, garantindo a continuidade operacional do sistema. Além disso, a simplicidade do Raft facilita a compreensão do protocolo, permitindo uma implementação mais precisa e robusta.

A escolha do Raft em relação a outros protocolos de consenso se dá principalmente pela facilidade da sua compreensão, em especial quando comparado com outros protocolos como o Paxos. As principais considerações pela sua escolha foram:

- Simplicidade e Entendimento: O Raft é reconhecido por sua clareza e simplicidade conceitual, facilitando o entendimento e implementação. Em um projeto de tamanha importância como um sistema de mensageria distribuída, a simplicidade do Raft torna-se uma vantagem significativa.

- Processo de Eleição Determinística: O Raft utiliza um processo de eleição determinística, evitando ambiguidades associadas à eleição em ambientes complexos. Esse determinismo é crucial para manter a coerência do sistema em situações de falha.

- Manutenção e Evolução do Código: A clareza do Raft simplifica a manutenção do código ao longo do tempo. Compreender e modificar o código é mais acessível, resultando em um desenvolvimento mais eficiente e menos propenso a erros.

- Facilidade de Implementação no Contexto do Apache Kafka: Dado que o Raft foi projetado para ser acessível e compreensível, sua integração com o Apache Kafka, um sistema de mensageria distribuída, é mais direta. A arquitetura do Raft alinha-se de maneira eficiente com os requisitos de replicação do Apache Kafka.

## 3.5 Implementação

A aplicação foi desenvolvida em Go originalmente por se tratar de uma linguagem compilada e de simples compreensão. A linguagem conta com construções primitivas de concorrência, que é um dos pontos essenciais para a implementação de um sistema de mensageria distribuída. Além disso, a linguagem conta com uma biblioteca padrão extensiva que facilita o desenvolvimento de servidores web.

O servidor conta com uma API REST para gerenciamento de tópicos e um endpoint SSE para comunicação com os clientes. A API REST é responsável por gerenciar os tópicos, permitindo a criação, listagem e remoção de tópicos, além de publicação de mensagens. O endpoint SSE é responsável por distribuir as mensagens para os clientes conectados.

A premissa base do sistema é a distribuição por tópicos, o que facilita o roteamento e a distribuição de mensagens entre os clientes. Cada tópico atua como uma fila de mensagens, de contexto específico e com um conjunto de clientes inscritos. Quando uma mensagem é publicada em um tópico, ela é distribuída para todos os clientes inscritos no tópico.

Esse modelo de tópicos resulta em uma distribuição de mensagens mais eficiente, uma vez que as mensagens são distribuídas apenas para os clientes inscritos no tópico, e não para todos os clientes conectados ao servidor. Além disso, esse modelo permite que os clientes se inscrevam em tópicos específicos, recebendo apenas as mensagens que são relevantes para eles.

```mermaid
sequenceDiagram
  participant Cliente
  participant REPL
  participant Servidor

  Cliente->>REPL: Realiza uma requisição
  REPL->>Cliente: Inicia uma conexão SSE
  loop Atualizações do tópico
    Servidor->>REPL: Envia atualizações do tópico
    REPL->>Cliente: Distribui a atualização para os clientes conectados
  end
```

Além disso, o sistema conta com um processo de replicação de mensagens entre os nós do cluster, garantindo a consistência entre os nós e a entrega das mensagens para os tópicos. O processo de replicação é feito através do protocolo de consenso Raft, onde no modo cluster todas as atualizações de estado do sistema são processadas através de uma máquina de estado finita determinística, da qual processa cada operação sequencialmente e garante a consistência entre os nós do cluster.

## 3.6 Comparação entre sistemas de mensageria

Abaixo temos uma tabela comparativa entre o sistema desenvolvido neste trabalho (REPL), o Kafka e o Redis Pub/Sub.

| Métrica                       | Kafka             | Redis Pub/Sub     | REPL (Aplicação)  |
| ----------------------------- | ----------------- | ----------------- | ----------------- |
| Cluster                       | Sim               | Sim               | Sim               |
| Modelo de mensageria          | Publish/Subscribe | Publish/Subscribe | Publish/Subscribe |
| Protocolo de consenso         | Zookeeper         | N/A               | Raft              |
| Linguagem de programação      | Java/Scala        | C                 | Go                |
| Protocolo de comunicação      | TCP               | TCP               | HTTP              |
| Mensagens                     | Bytes             | Bytes             | JSON              |
| Persistência                  | Sim               | Sim               | Não               |
| Tópicos                       | Sim               | Sim               | Sim               |
| Garante a entrega da mensagem | Sim               | Não               | Não               |
| Garante a ordem das mensagens | Sim               | Não               | Não               |

## 3.7 Desenvolvimento e arquitetura da aplicação

A linguagem escolhida para o desenvolvimento da aplicação foi a linguagem Go, por se tratar de uma linguagem compilada, com gerenciamento de memória e de simples compreensão. O Go conta com estruturas primitivas de concorrência como rotinas de _background_ e canais de comunicação para envio de dados e sincronização de threads, pontos cruciais para o desenvolvimento de uma aplicação que lida com larga escala de dados e concorrência.

A aplicação pode ser executada em dois modos, sendo eles _standalone_ e em cluster. Em modo stand-alone a aplicação executa em uma única máquina, nesse modo a performance com relação a publicação de mensagens é maior do que em modo cluster, pois não necessita de distribuição e replicação de mensagens entre máquinas.

Em modo cluster a aplicação executa em várias máquinas, e é possível adicionar mais nós ao cluster. Nesse modo a aplicação conta com um processo de replicação de mensagens entre os nós utilizando o Raft como protocolo de consenso, garantindo a consistência entre os nós e a entrega das mensagens para os tópicos. Cada um dos modos conta com prós e contras, sendo o modo stand-alone mais eficiente para publicação de mensagens, e o modo cluster suportando mais conexões.

### 3.7.1 Estruturas de distribuição de mensagens

Durante o desenvolvimento, um dos principais pontos de atenção era o desempenho e eficiência da aplicação, uma vez que ela lida com uma grande quantidade de dados e precisa ser escalável. Para isso, foram realizados testes de desempenho para avaliar estruturas alternativas de concorrência e distribuição de mensagens.

A primeira alternativa foi utilizar uma estrutura de distribuição de dados no padrão _broadcast_, onde um canal central distribuí as mensagens para os clientes conectados de maneira síncrona. Apesar de ser de fácil compreensão ela se mostrou ineficiente para o propósito da aplicação, uma vez que chamadas bloqueantes de escrita entre diferentes threads resultava em um decréscimo de performance conforme o número de clientes aumentava na aplicação.

Foram realizados outros testes com essa mesma estrutura, realizando a escrita das mensagens em uma thread de execução separada, para o aumento da performance. Isso resultou em uma melhora da performance, entretanto o custo dessa alternativa foi o aumento de utilização de recursos computacionais. O aumento do número de threads de execução resultou em um custo de consumo de memória e processamento, em especial, para o runtime da própria linguagem. Com a execução de mais threads e mais alocação de memória, o runtime passou a consumir mais recursos computacionais para gerenciar os recursos utilizados pela aplicação, resultando em lentidão para desalocação de recursos.

A estrutura mais eficiente para o nosso caso de uso foi a distribuição de mensagens através de um "broker". Um broker de mensagens é uma estrutura responsável por armazenar e distribuir mensagens para os respectivos clientes. Essa estrutura é utilizada em sistemas de mensageria como o Apache Kafka, e se mostrou eficiente para o nosso caso de uso. A estrutura de broker de mensagens é composta por um servidor de mensageria, responsável por receber as mensagens e distribuí-las para os clientes conectados. Essa estrutura é mais eficiente para o nosso caso de uso, uma vez que a distribuição de mensagens é feita de maneira assíncrona, e o servidor de mensageria é responsável por gerenciar a distribuição de mensagens para os clientes conectados.

A estrutura de broker na aplicação consiste em uma estrutura de dados que possui uma fila interna de mensagens que é alterada quando uma requisição de publicação para um determinado tópico é realizada. Essa fila armazena as mensagens para serem consumidas pelos clientes posteriormente. O broker executa a distribuição de mensagens removendo os primeiros items que foram adicionados na fila e distribuindo para os clientes conectados no tópico.

Essa estrutura se mostrou muito eficiente para a aplicação, resultando em uma melhora significativa da performance. Por se tratar de uma distribuição assíncrona, a estrutura pode armazenar as mensagens em uma fila interna e distribuir para os clientes conectados posteriormente, contrário a estrutura de _broadcast_, essa alternativa pode distribuir mensagens em batches, reduzindo operações de sincronização na aplicação e chamadas do sistema operacional para escrever nos sockets dos clientes conectados.

### 3.7.2 Análise de performance e otimizações

Um dos principais pontos de atenção durante o desenvolvimento da aplicação foi a performance de distribuição das mensagens para os clientes conectados. Para isso, foram realizados testes de desempenho para avaliar a performance da aplicação e identificar gargalos de performance, entretanto, também foram necessárias inspeções no funcionamento da aplicação, como análise de CPU e análise de alocação de memória durante a execução da aplicação.

A técnica utilizada para inspeção da aplicação é foi a chamada _profiling_, ela consiste de executar a aplicação em um ambiente de testes e gerar relatórios de performance durante a execução da aplicação. Para isso, foram utilizadas ferramentas de profiling da própria linguagem Go, como o _pprof_ e o _trace_, que são ferramentas de profiling nativas da linguagem. Essas ferramentas são capazes de gerar relatórios de performance enquanto a aplicação é executada, com esses relatórios é possível ver métricas úteis para a otimização do código, como alocação de memória e tempo de execução de funções.

![Profiling da memória](images/heap-profile.jpeg)

A partir dos relatórios gerados pelo _profiling_ da aplicação foi possível analisar e otimizar pontos que prejudicavam a performance. O ponto principal de otimização foi com relação a chamadas do sistema operacional (_syscalls_), observando a performance de cada chamada e otimizando o código para reduzir o número de chamadas.

Além das chamadas de sistema operacional também foram otimizadas operações dentro da aplicação, como operações de serializar JSON. Durante os teste foi identificado que a escrita de mensagens para os clientes realizava operações de transformar uma estrutura de dados para uma string por $N$ iterações para $N$ clientes, resultando em uma complexidade assintótica de $O(n^2)$.

A solução interna para esse problema de performance foi de publicar as mensagens, que anteriormente eram estruturas de dados, diretamente em formato de strings para o broker, removendo assim a necessidade da aplicação de serializar as mensagens para cada cliente conectado. Essa otimização resultou em uma melhora significativa da performance, em especial para os casos onde o servidor possuía uma grande quantidade de clientes conectados.

## 4. Resultados, análise e discussão

Os testes de desempenho foram realizados utilizando a ferramenta [wrk](https://github.com/wg/wrk) para requisições HTTP e um cliente SSE desenvolvido em Go para simular os clientes. Os testes foram realizados em um computador com processador Intel I5-1210U e 16GB de memória RAM, utilizando o sistema operacional Linux Ubuntu 22.04.

## 4.1 Testes de desempenho

Os testes foram realizados em pequenas baterias, com diferentes quantidades de clientes conectados, aplicações e linguagens de programação diferentes. Contando com implementações em NodeJS e Python. Os testes consistem em 5 baterias, contando com 50, 100, 500, 1000 e 2000 conexões para cada servidor. Cada bateria consiste em um teste de carga com intervalo de 10 segundos para cada aplicação, onde o intuito foi medir a quantidade de mensagens publicadas por segundo, latência e utilização de recursos da máquina. Esse teste é demonstrativo e compara a performance da aplicação desenvolvida em modo stand-alone, executando em uma única máquina.

### 4.1.1 Tabela de performance do NodeJS

| Clientes | Requisições (RP/s) | Latência (1k msg/s) | Taxa (msg/ms) | CPU   | Memória |
| -------- | ------------------ | ------------------- | ------------- | ----- | ------- |
| 50       | 9.601              | 1.1s                | 890           | 37.3% | 0.4%    |
| 100      | 6.818              | 1.4s                | 720           | 70.1% | 0.5%    |
| 500      | 1.475              | 6.2s                | 160           | 84.9% | 0.5%    |
| 1000     | 765                | 12.9                | 77            | 87%   | 0.6%    |
| 2000     | 386                | 25s                 | 38            | 93.3% | 0.7%    |

### 4.1.2 Tabela de performance do Python

| Clientes | Requisições (RP/s) | Latência (1k msg/s) | Taxa (msg/ms) | CPU   | Memória |
| -------- | ------------------ | ------------------- | ------------- | ----- | ------- |
| 50       | 2.044              | 1.8s                | 550           | 31.3% | 0.3%    |
| 100      | 1.618              | 2.5s                | 400           | 55.4% | 0.3%    |
| 500      | 700                | 8.7s                | 113           | 81.8% | 0.3%    |
| 1000     | 383                | 19.3s               | 52            | 93.8% | 0.4%    |
| 2000     | 198                | 41s                 | 24            | 96.9% | 0.6%    |

### 4.1.3 Tabela comparativa de performance do REPL

| Clientes | Requisições (RP/s) | Latência (1k msg/s) | Taxa (msg/ms) | CPU    | Memória |
| -------- | ------------------ | ------------------- | ------------- | ------ | ------- |
| 50       | 106.598            | 0.1s                | 10.000        | 144.0% | 3%      |
| 100      | 56.927             | 0.1s                | 10.000        | 231%   | 1.8%    |
| 500      | 9.534              | 0.15s               | 6.666         | 356%   | 0.4%    |
| 1000     | 4.666              | 0.3s                | 3.333         | 300%   | 0.6%    |
| 2000     | 2.514              | 0.6s                | 1.666         | 268%   | 1.1%    |

## 4.1.4 Gráficos de performance

| Requisições por segundo                    | Latência                        | Taxa de mensagens                     |
| ------------------------------------------ | ------------------------------- | ------------------------------------- |
| ![Requisições por segundo](charts/rps.png) | ![Latência](charts/latency.png) | ![Taxa de mensagens](charts/rate.png) |

## 4.2 Testes de integração

Realizamos também testes de integração da aplicação foram desenvolvidas 3 demonstrações, para exemplificar os modelos arquiteturais descritos e a performance de cada um:

- Aplicação 1: NodeJS monolítica, responsável por gerenciar os tópicos e distribuir as mensagens para os clientes conectados;
- Aplicação 2: NodeJS utilizando um sistema de mensageria (Redis) para distribuição de mensagens;
- Aplicação 3: NodeJS utilizando o serviço de mensageria descrito neste trabalho;

Assim como no teste anterior, cada bateria consiste em um teste de carga com intervalo de 10 segundos para cada aplicação, onde o intuito foi medir a quantidade de requisições por segundo e a utilização de recursos da máquina, com a quantidade de clientes conectados sendo 50, 100, 500 e 1000 respectivamente.

Os resultados do teste de integração são apresentados na tabela abaixo:

## 4.2.1 Primeira bateria de testes - 50 conexões

| Aplicação   | Número de conexões | Requisições por segundo | Utilização de CPU | Utilização de memória |
| ----------- | ------------------ | ----------------------- | ----------------- | --------------------- |
| Aplicação 1 | 50                 | x                       | x                 | x                     |
| Aplicação 2 | 50                 | x                       | x                 | x                     |
| Aplicação 3 | 50                 | x                       | x                 | x                     |

## 4.2.2 Segunda bateria de testes - 100 conexões

| Aplicação   | Número de conexões | Requisições por segundo | Utilização de CPU | Utilização de memória |
| ----------- | ------------------ | ----------------------- | ----------------- | --------------------- |
| Aplicação 1 | 100                | x                       | x                 | x                     |
| Aplicação 2 | 100                | x                       | x                 | x                     |
| Aplicação 3 | 100                | x                       | x                 | x                     |

## 4.2.3 Terceira bateria de testes - 500 conexões

| Aplicação   | Número de conexões | Requisições por segundo | Utilização de CPU | Utilização de memória |
| ----------- | ------------------ | ----------------------- | ----------------- | --------------------- |
| Aplicação 1 | 500                | x                       | x                 | x                     |
| Aplicação 2 | 500                | x                       | x                 | x                     |
| Aplicação 3 | 500                | x                       | x                 | x                     |

## 4.2.4 Quarta bateria de testes - 1000 conexões

| Aplicação   | Número de conexões | Requisições por segundo | Utilização de CPU | Utilização de memória |
| ----------- | ------------------ | ----------------------- | ----------------- | --------------------- |
| Aplicação 1 | 1000               | x                       | x                 | x                     |
| Aplicação 2 | 1000               | x                       | x                 | x                     |
| Aplicação 3 | 1000               | x                       | x                 | x                     |

## Desenvolvimento (Tarefas)

- [x] Finalização do modelo de arquitetura do sistema;
- [x] Explicação do protocolo SSE e descrição do motivo pelo qual a gente escolheu ele;
- [x] Explicação a respeito do funcionamento do sistema (divisão de tópicos para clientes conectados);
- [x] Tabela comparativa dos principais sistemas de mensageria (Kafka, Redis Pub/Sub, e a nossa aplicação);
- [x] Descrição dos requisitos não funcionais: limitações do sistema;
  - Limite do tamanho de mensagens
  - O sistema vai salvar as mensagens?
  - O sistema vai ter um limite de conexões?
- [x] Descrição da implementação do sistema
  - Como o sistema foi implementado
  - Como funciona a distribuição de mensagens
  - Como funciona a divisão de tópicos

## Tarefas (escrita)

- [ ] Resultados, análise e discussão:
  - [x] Finalização da implementação do sistema;
  - [x] Aplicações demo para testes de desempenho;
  - [ ] Dados dos testes de desempenho;
  - [ ] Análise dos dados dos testes de desempenho;
  - [ ] Discussão dos resultados (quantitativo): performance do sistema e escalabilidade;
  - [ ] Discussão dos resultados (qualitativo): facilidade de implementação e manutenção;
- [ ] Conclusão
