# Aplicações Distribuídas

Bem-vindo ao repositório **Aplicações Distribuídas**! Este repositório contém três projetos focados em princípios de computação distribuída utilizando Python.

This file also exists in [English](README.md)

## Índice
1. [Projeto 1](#projeto-1)
2. [Projeto 2](#projeto-2)
3. [Projeto 3](#projeto-3)

---

## Projeto 1

### Visão Geral
O **Projeto 1** desenvolve uma aplicação distribuída Coin Center que simula funcionalidades básicas como a gestão de ativos, a realização de transações e o controlo dos saldos dos clientes. Introduz conceitos fundamentais de comunicação cliente-servidor através de uma rede.

### Funcionalidades
- Implementação de sockets TCP para comunicação cliente-servidor.
- Funcionalidades básicas para adicionar, remover e obter informações sobre ativos.
- Suporte a múltiplas interações com ativos.
- Inclui papéis de gestor e utilizador com funções distintas.

### Ficheiros Principais
- [`sock_utils.py`](project1/sock_utils.py): Utilitários para criação de sockets TCP.
- [`coincenter_client.py`](project1/coincenter_client.py): Implementa um cliente para o Coin Center.
- [`coincenter_server.py`](project1/coincenter_server.py): Implementação do servidor que trata os pedidos.

---

## Projeto 2

### Visão Geral
No **Projeto 2**, o Coin Center é estendido com padrões de design baseados em skeletons e lógica de comunicação refinada. Este projeto enfatiza a separação da lógica de negócio e o tratamento de mensagens distribuídas.

### Funcionalidades
- Introdução de um `CoinCenterSkeleton` para gestão da lógica central.
- Implementação de uma classe `NetServer` para gerir eventos de rede.
- Maior modularidade através da separação entre a lógica de rede e da aplicação.
- Suporte eficaz para adição e remoção de ativos, bem como pedidos dos utilizadores.

### Ficheiros Principais
- [`coincenter_skel.py`](project2/coincenter_skel.py): Skeleton responsável pela lógica de negócio.
- [`coincenter_server.py`](project2/coincenter_server.py): Implementa o servidor integrando o skeleton com a camada de rede.
- [`sock_utils.py`](project2/sock_utils.py): Utilitário de sockets TCP para comunicação em rede.

---

## Projeto 3

### Visão Geral
O **Projeto 3** transforma o Coin Center num microsserviço RESTful utilizando Flask. Evolui para um sistema distribuído pronto para produção, com armazenamento persistente e endpoints de API.

### Funcionalidades
- Arquitetura RESTful baseada em Flask para gestão de pedidos HTTP.
- Integração com SQLite para armazenamento persistente em base de dados.
- Endpoints de API para gestão de clientes, ativos e transações.
- Integração com Zookeeper (`KazooClient`) para sincronização e gestão distribuída.

### Ficheiros Principais
- [`coincenter_flask.py`](project3/coincenter_flask.py): Servidor Flask responsável pelas rotas da API.
- [`setup_db.py`](project3/setup_db.py): Responsável pela configuração e ligação à base de dados.
- [`coincenter_data.py`](project3/coincenter_data.py): Contém funções de base de dados, como queries e gestão de ativos.

---

## Contribuições
Contribuições são bem-vindas! Se tiveres ideias ou encontrares algum problema, sente-te à vontade para abrir um *pull request* ou criar uma *issue*.

## Licença
Este projeto não possui licença definida. Para direitos de utilização, por favor contacta o proprietário do repositório.

---

**Proprietário do Repositório:** [vitoriateixeiracorreia](https://github.com/vitoriateixeiracorreia)
