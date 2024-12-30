# Desafio: incrementando o sistema bancário
# Precisamos implementar o sistema UML apresentado na imagem, utilizando POO no sistema bancário desenvolvido anteriormente

import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class Deposito:
    def __init__(self, valor):
        _valor = valor


class Saque:
    def __init__(self, valor):
        _valor = valor


class Transacao(ABC, Deposito, Saque):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def registrar(self):
        pass


class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

    @property
    def contas(self):
        return self._contas


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self._cpf

    @property
    def nome(self):
        return self._nome

    @property
    def data_nascimento(self):
        return self._data_nascimento


class Historico:
    def adicionar_transacao(self, transacao):
        pass


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print('Operação falhou! Você não tem saldo suficiente.')

        elif valor < 0:
            print('Operação falhou! O valor informado não é válido.')

        else:
            self._saldo -= valor
            print("Saque realizado com sucesso.")
            return True

        return False

    def depositar(self, valor):
        if valor < 0:
            print("Operação falhou! O valor informado é inválido.")
        else:
            self._saldo += valor
            print("Depósito realizado com sucesso.")
            return True
        return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente,  limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    @property
    def limite(self):
        return self._limite

    @property
    def limite_saques(self):
        return self._limite_saques

    def sacar(self, valor):

        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao['tipo']
                == Saque.__name__]
        )

        excedeu_saldo = valor > self.saldo
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_saldo:
            print('Operação falhou! Você não tem saldo suficiente.')

        elif excedeu_limite:
            print('Opoeração falhou! O valor do saque excede o limite.')

        elif excedeu_saques:
            print('Operação falhou! Número máximo de saques excedido.')

        elif valor < 0:
            print('Operação falhou! O valor informado é inválido.')

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M%s"),
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():

    menu = """ 
        [d]\tDepositar
        [s]\tSacar
        [e]\tExtrato
        [u]\tCriar Usuário
        [c]\tCriar Conta
        [mc]\tMostrar Contas
        [q]\tSair

        => """
    return input(textwrap.dedent(menu))


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Operação falou. O cliente não possui conta neste banco.")
        return False

    else:
        print(f"O cliente '{cliente.nome}' possui as contas:")
        for conta in cliente.contas:
            print(conta)
        conta = int(
            input("Digite a conta que gostaria de utilizar para esta operação: "))

        return cliente.contas[conta-1]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return False

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        print("Operação falhou! Este usuário não possui conta neste banco.")
        return False
    else:
        cliente.realizar_transacao(conta, transacao)
        return True


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return False

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        print("Operação falhou! Este usuário não possui conta neste banco.")
        return False
    else:
        cliente.realizar_transacao(conta, transacao)
        return True

# a função extrato deve ser feita de modo que os parametros sejam positional only e keyword only


def visualizar_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Operação falhou! Cliente não encontrado.")
        return False

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        print('Operação falhou! Este usuário não possui conta neste banco.')
        return False
    else:
        print('\n ============== Extrato ===============')
        transacoes = conta.historico.transacoes

        extrato = ""
        if not transacoes:
            extrato = 'Não foram realizados movimentações.'
        else:
            for transacao in transacoes:
                extrato += f'\n{transacao['tipo']
                                }:\n\tR${transacao['valor']:.2f}'

        print(extrato)
        print(f'\nSaldo:\n\tR$ {conta.saldo:.2f}')
        print('\n ======================================')
        return True


# ==========================================
# aqui serão criadas as novas funções desta versão.

# criando a função para criar usuário com os atributos de nome, data de nascimento, cpf (sem repetição) e endereço
def criar_usuario(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Operação falhou! Este cliente já esta cadastrado no banco.")
        return False
    else:
        nome = input('Informe o nome completo: ')
        data_nascimento = input('Informe a data de nascimento (dd-mm-aaaa): ')
        endereco = input(
            'Informe o endereço (lagradouro, numero, bairro - cidade/sigla estado): ')

        cliente = PessoaFisica(
            nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

        clientes.append(cliente)
        print('Cliente criado com sucesso.')
        return True


# criando conta corrente composta por: agência, número da conta e usuário. O número da conta deve ser sequencial, iniciado em 1. O número da agência é fixo: '0001'. O usuário pode ter mais de uma conta, mas  uma conta pertence a somente um usuário
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Operação falhou! Cliente não encontrado.")
        return False
    else:
        conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
        contas.append(conta)
        cliente.adicionar_conta(conta)
        print('Conta criada com sucesso.')
        return True


def filtrar_cliente(cpf, clientes):

    for cliente in clientes:
        if cpf == cliente.cpf:
            return cliente

    return False


def listar_contas(contas):
    for conta in contas:
        print("="*100)
        print(textwrap.dedent(str(conta)))


def main():

    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 'd':
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == 'e':
            visualizar_extrato(clientes)

        elif opcao == 'u':
            criar_usuario(clientes)

        elif opcao == 'c':
            numero_conta = len(contas)+1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == 'mc':
            listar_contas(contas)

        elif opcao == 'q':
            break

        else:
            print('Operação inválida, por favor selecione novamente a operação desejada.')


main()
