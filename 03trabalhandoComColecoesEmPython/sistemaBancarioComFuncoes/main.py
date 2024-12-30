# Desafio: incrementando o sistema bancário
# Precisamos implementar o sistema UML apresentado na imagem, utilizando POO no sistema bancário desenvolvido anteriormente

import textwrap


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


# a funcao saque deve receber apenas por nome (keyword only)
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print('Operação falhou! Você não tem saldo suficiente.')

    elif excedeu_limite:
        print('Opoeração falhou! O valor do saque excede o limite.')

    elif excedeu_saques:
        print('Operação falhou! Número máximo de saques excedido.')

    elif valor > 0:
        saldo -= valor
        extrato += f'\tSaque:\t\tR$ {valor:.2f}\n'
        numero_saques += 1

    else:
        print('Operação falhou! O valor informado é inválido.')

    return saldo, extrato


# a função deposito deve ser feita de modo que os parametros sejam somente positional only
def depositar(saldo, valor, extrato, /):

    if valor < 0:
        print("Operação falhou! O valor informado é inválido.")
    else:
        saldo += valor
        extrato += f"\tDeposito:\tR$ {valor:.2f}\n"

    return saldo, extrato


# a função extrato deve ser feita de modo que os parametros sejam positional only e keyword only
def visualizar_extrato(saldo, /, *, extrato):
    print('\n ============== Extrato ===============')
    print('Não foram realizados movimentações.' if not extrato else extrato)
    print(f'\tSaldo:\t\tR$ {saldo:.2f}')
    print('=========================================')


# ==========================================
# aqui serão criadas as novas funções desta versão.

# criando a função para criar usuário com os atributos de nome, data de nascimento, cpf (sem repetição) e endereço
def criar_usuario(lista_de_usuarios):
    nome = input('Nome do novo usuário: Brenddon Oliveira\n')
    data_de_nascimento = input('Data de nascimento: dd-mm-aa\n')
    cpf = input('CPF: 11122233344\n')
    for user in lista_de_usuarios:
        if cpf == user['cpf']:
            print('Operação falhou! Já existe um usuário com este CPF.')
            return lista_de_usuarios
    endereco = input(
        'Endereço: logradouro, número - bairro - cidade/sigla do estado.\n')

    novo_usuario = {'nome': nome, 'data_de_nascimento': data_de_nascimento,
                    'cpf': cpf, 'endereco': endereco}
    lista_de_usuarios.append(novo_usuario)
    return lista_de_usuarios


# criando conta corrente composta por: agência, número da conta e usuário. O número da conta deve ser sequencial, iniciado em 1. O número da agência é fixo: '0001'. O usuário pode ter mais de uma conta, mas  uma conta pertence a somente um usuário
def criar_conta(lista_de_contas, lista_de_usuarios):
    if not lista_de_contas:
        conta = 1
    else:
        # pegando a última conta criada
        conta = len(lista_de_contas) + 1

    agencia = '0001'

    # obtendo lista de cpfs
    lista_cpf = pegar_listas_de_cpfs(lista_de_usuarios)

    cpf = input('CPF a vincular na conta: 11122233344\nCPF: ')
    if cpf in lista_cpf:
        conta = {'id_usuario': cpf, 'conta': conta, 'agencia': agencia}
        lista_de_contas.append(conta)
        return lista_de_contas
    else:
        print('Operação falhou! Não existe um usuário cadastrado com este CPF. Crie um usuário antes de realizar esta operação.')
        return lista_de_contas


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


def pegar_listas_de_cpfs(lista_de_usuarios):
    lista_cpf = []
    for usuario in lista_de_usuarios:
        lista_cpf.append(usuario['cpf'])

    return lista_cpf


def main():

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    lista_de_usuarios = []
    lista_de_contas = []

    while True:
        opcao = menu()

        if opcao == 'd':
            valor = float(input("Informe o valor de deposito: R$ "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: R$ "))
            saldo, extrato = sacar(saldo=saldo, valor=valor, limite=limite,
                                   numero_saques=numero_saques, limite_saques=LIMITE_SAQUES, extrato=extrato)

        elif opcao == 'e':
            visualizar_extrato(saldo, extrato=extrato)

        elif opcao == 'u':
            lista_de_usuarios = criar_usuario(lista_de_usuarios)

        elif opcao == 'c':
            lista_de_contas = criar_conta(lista_de_contas, lista_de_usuarios)

        elif opcao == 'mu':
            mostrar_usuarios(lista_de_usuarios)

        elif opcao == 'mc':
            mostrar_contas(lista_de_contas)

        elif opcao == 'q':
            break

        else:
            print('Operação inválida, por favor selecione novamente a operação desejada.')


main()
