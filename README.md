# 🏦 Sistema Bancário em Python (POO)

Projeto desenvolvido em **Python** utilizando os conceitos de **Programação Orientada a Objetos (POO)**, com simulação de operações bancárias via terminal.

O sistema permite:

- Criar clientes
- Criar contas correntes
- Realizar depósitos
- Realizar saques com limite
- Exibir extrato
- Listar contas cadastradas

---

## 📌 Conceitos Aplicados

- Classes e Objetos
- Herança
- Polimorfismo
- Encapsulamento
- Classes Abstratas (ABC)
- Métodos especiais (`__str__`)
- Manipulação de listas e dicionários
- Registro de histórico com data/hora

---

## 🏗️ Estrutura do Projeto

### 🔹 Classes principais

| `Conta` | Classe base para contas bancárias |
| `ContaCorrente` | Conta com limite de saque e limite diário |
| `Cliente` | Representa um cliente do banco |
| `PessoaFisica` | Cliente com CPF |
| `Historico` | Armazena as transações realizadas |
| `Transacao` | Classe abstrata para operações |
| `Saque` | Implementa operação de saque |
| `Deposito` | Implementa operação de depósito |

---

## 🚀 Funcionalidades

### 👤 Cliente
- Cadastro de novo usuário
- Associação de conta ao cliente

### 💰 Conta
- Depósito de valores positivos
- Saque com:
  - Limite de valor (R$500 padrão)
  - Limite de 3 saques por dia
- Exibição de extrato
- Registro automático de transações com data e hora

---

## 📋 Menu do Sistema
[d] Depositar
[s] Sacar
[e] Extrato
[nc] Nova conta
[lc] Listar contas
[nu] Novo usuário
[q] Sair

## 🛠️ Tecnologias Utilizadas
Python 3
Módulos nativos:
- abc
- datetime
- textwrap

## 📚 Regras de Negócio Implementadas

- Não permite saque maior que o saldo

- Não permite valores negativos

- Limite padrão de saque: R$ 500,00

- Limite de 3 saques por dia

- Histórico registra:

1) Tipo da transação

2) Valor

3) Data e hora

## 🎯 Objetivo do Projeto

Este projeto tem finalidade educacional e foi desenvolvido para praticar:

- Modelagem de domínio

- Organização de código

- Aplicação de boas práticas de POO

- Simulação de regras de negócio reais
