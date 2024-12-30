# Desafio: incrementando o sistema bancário
# Precisamos implementar o sistema UML apresentado na imagem, utilizando POO no sistema bancário desenvolvido anteriormente

import textwrap
from abc import ABC
from datetime import datatime


class Deposito:
    def __init__(self, valor):
        _valor = valor


class Saque:
    def __init__(self, valor):
        _valor = valor


class Transacao(ABC, Deposito, Saque):
    @asbstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def registrar(self):
        pass


class Cliente(Transacao):
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)


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
        super.__init__(numero, cliente)
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
                "data": datatime.now().strftime("%d-%m-%Y %H:%M%s"),
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
        [mu]\tMostrar Usuários
        [mc]\tMostrar Contas
        [q]\tSair

        => """
    return input(textwrap.dedent(menu))


def recuperar_conta_cliente(cliente):
    if not cliente.conta:
        print("Operação falou. O cliente não possui conta neste banco.")
        return False

    else:
        print(f"O cliente '{cliente.name}' possui as contas:")
        for conta in cliente.conta:
            print(conta)
        conta = int(
            input("Qual conta gostaria de utilizar para esta operação?"))
        return conta


def depositar(clientes):
    cpf = input("Informe o CPF do cliente")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        print("Operação falhou. Este usuário não possui conta neste banco.")
        return False
    else:
        cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        print("Operação falhou. Este usuário não possui conta neste banco.")
        return False
    else:
        cliente.realizar_transacao(conta, transacao)

# a função extrato deve ser feita de modo que os parametros sejam positional only e keyword only


def visualizar_extrato(clientes):
    print('\n ============== Extrato ===============')
    print('Não foram realizados movimentações.' if not extrato else extrato)
    print(f'\tSaldo:\t\tR$ {saldo:.2f}')
    print('=========================================')


# ==========================================
# aqui serão criadas as novas funções desta versão.

# criando a função para criar usuário com os atributos de nome, data de nascimento, cpf (sem repetição) e endereço
def criar_usuario(clientes):

    nome = input('Nome do novo usuário: Brenddon Oliveira\n')
    data_de_nascimento = input('Data de nascimento: dd-mm-aa\n')
    cpf = input('CPF: 11122233344\n')
    for user in clientes:
        if cpf == user['cpf']:
            print('Operação falhou! Já existe um usuário com este CPF.')
            return False
    endereco = input(
        'Endereço: logradouro, número - bairro - cidade/sigla do estado.\n')

    novo_usuario = {'nome': nome, 'data_de_nascimento': data_de_nascimento,
                    'cpf': cpf, 'endereco': endereco}
    clientes.append(novo_usuario)
    return True


# criando conta corrente composta por: agência, número da conta e usuário. O número da conta deve ser sequencial, iniciado em 1. O número da agência é fixo: '0001'. O usuário pode ter mais de uma conta, mas  uma conta pertence a somente um usuário
def criar_conta(contas, clientes):
    if not contas:
        conta = 1
    else:
        # pegando a última conta criada
        conta = len(contas) + 1

    agencia = '0001'

    # obtendo lista de cpfs
    lista_cpf = pegar_listas_de_cpfs(clientes)

    cpf = input('CPF a vincular na conta: 11122233344\nCPF: ')
    if cpf in lista_cpf:
        conta = {'id_usuario': cpf, 'conta': conta, 'agencia': agencia}
        contas.append(conta)
        return True
    else:
        print('Operação falhou! Não existe um usuário cadastrado com este CPF. Crie um usuário antes de realizar esta operação.')
        return False


# extra ====================
def mostrar_usuarios(lista_de_usuarios):
    if not lista_de_usuarios:
        print('Lista de usuários ainda está vazia.')
    for usuario in lista_de_usuarios:
        for key, value in usuario.items():
            print(f'{key}: {value}')
        print('')


def mostrar_contas(lista_de_contas):
    if not lista_de_contas:
        print('Lista de contas ainda está vazia.')
    for conta in lista_de_contas:
        for key, value in conta.items():
            print(f'{key}: {value}')
        print('')


def filtrar_cliente(cpf, clientes):

    for cliente in clientes:
        if cpf == cliente.cpf:
            return cliente

    return False


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
            criar_conta(contas, clientes)

        elif opcao == 'mu':
            mostrar_usuarios(lista_de_usuarios)

        elif opcao == 'mc':
            mostrar_contas(lista_de_contas)

        elif opcao == 'q':
            break

        else:
            print('Operação inválida, por favor selecione novamente a operação desejada.')


main()
