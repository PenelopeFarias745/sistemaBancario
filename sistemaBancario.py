from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

class Conta():
    def __init__(self, numero, cliente):
        self._cliente = cliente
        self._numero = numero
        self._saldo = 0
        self._agencia = "0001"
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def historico(self):
        return self._historico
    

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("Operação falhou. Saldo insuficiente")
        elif valor > 0:
            self._saldo -= valor
            print(f"Saque de R${valor:.2f} realizado com sucesso!")
            return True
        else:
            print("Operação falhou. Valor inválido.")
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"Depósito de R${valor:.2f} realizado com sucesso!")
        else:
            print("Operação falhou. Valor inválido.")
            return False
        return True

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacao if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques
        
        if excedeu_limite:
            print("A operação falhou! O valor do saque excedeu o limite.")
        elif excedeu_saques:
            print("A operação falhou! Número de saques excedidos por hoje.")
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

    
    def depositar(self, valor):
            if valor > 0:
                self._saldo += valor
                return print(f"Depósito de R${valor:.2f} realizado com sucesso!")
            else:
                return print("Número inválido. Tente novamente.")
            
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transcoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })

class Transacao(ABC):
    @property
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init___(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

    
class Deposito(Transacao):
    def __init___(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    menu = """\n
    =============== MENU ===============
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """

    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]

    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente não possui conta.")
        return 
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o seu cpf = ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nCliente não encontrado")
        return
    valor = float(input("Informe o valor do depósito = "))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o seu cpf = ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nCliente não encontrado")
        return
    valor = float(input("Informe o valor do saque = "))
    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o seu cpf = ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nCliente não encontrado")
        return
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    print("\n=============== EXTRATO ===============")
    transacoes = conta.historico.transacoes
    extrato = ""
    if not transacoes:
        extrato = f"Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("===============================")

def criar_cliente(clientes):
    cpf = input("Informe o seu cpf = ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Já existe cliente com esse CPF.")
        return
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe sua data de nascimento: ")
    endereco = input("Informe o seu endereço: ")
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("Cliente criado com sucesso!")

def criar_conta(numero, clientes, contas):
    cpf = input("Informe o seu cpf = ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado, fluxo de criação de conta encerrado.")
        return
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero)
    contas.append(conta)
    cliente.contas.append(conta)
    print("A conta foi criada com sucesso!")

def listar_contas(contas):
    for conta in contas:
        print("="*100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()
        if opcao == "d":
            depositar(clientes)
        elif opcao == "s":
            sacar(clientes)
        elif opcao == "e":
            exibir_extrato(clientes)
        elif opcao == "nu":
            criar_cliente(clientes)
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            break
        else:
            print("\nOperação inválida, por favor selecione novamente a operação desejada.")

main()


    
    


    

