class Conta:
    def __init__(self, titular, numero, saldo=0):
        self.titular = titular
        self.numero = numero
        self.saldo = saldo
        self.extrato = ""
        self.numero_saques = 0
        self.limite = 500
        self.LIMITE_SAQUES = 3

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Depósito: R$ {valor:.2f}\n"
            return True
        else:
            return False

    def sacar(self, valor):
        if valor <= 0:
            return "valor_invalido"
        elif valor > self.saldo:
            return "saldo_insuficiente"
        elif valor > self.limite:
            return "limite_excedido"
        elif self.numero_saques >= self.LIMITE_SAQUES:
            return "limite_saques_excedido"
        else:
            self.saldo -= valor
            self.extrato += f"Saque: R$ {valor:.2f}\n"
            self.numero_saques += 1
            return "sucesso"

    def emitir_extrato(self):
        extrato = "\n================ EXTRATO ================\n"
        extrato += "Não foram realizadas movimentações.\n" if not self.extrato else self.extrato
        extrato += f"\nSaldo: R$ {self.saldo:.2f}\n"
        extrato += "==========================================\n"
        return extrato

class Banco:
    def __init__(self):
        self.contas = []

    def criar_conta(self, titular, numero):
        if any(conta.numero == numero for conta in self.contas):
            print("Uma conta com esse número já existe.")
            return None
        nova_conta = Conta(titular, numero)
        self.contas.append(nova_conta)
        return nova_conta

    def listar_contas(self):
        for conta in self.contas:
            print(f"Titular: {conta.titular}, Número da Conta: {conta.numero}, Saldo: R$ {conta.saldo:.2f}")

    def encontrar_conta(self, numero):
        for conta in self.contas:
            if conta.numero == numero:
                return conta
        return None

banco = Banco()
menu_principal = """
1 - Criar nova conta
2 - Acessar conta existente
3 - Listar contas
4 - Sair

=> """

menu_conta = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Voltar

=> """

while True:
    opcao_principal = input(menu_principal)

    if opcao_principal == "1":
        titular = input("Nome do titular: ")
        numero = input("Número da conta: ")
        if banco.criar_conta(titular, numero):
            print("Conta criada com sucesso!")
        else:
            print("Falha ao criar conta.")

    elif opcao_principal == "2":
        numero = input("Informe o número da conta: ")
        conta = banco.encontrar_conta(numero)
        if conta:
            while True:
                opcao_conta = input(menu_conta)
                if opcao_conta in ["d", "s"]:
                    valor_str = input("Informe o valor: ")
                    try:
                        valor = float(valor_str)
                        if opcao_conta == "d":
                            if conta.depositar(valor):
                                print("Depósito realizado com sucesso!")
                            else:
                                print("Operação falhou! O valor informado é inválido.")
                        elif opcao_conta == "s":
                            resultado = conta.sacar(valor)
                            if resultado == "sucesso":
                                print("Saque realizado com sucesso!")
                            else:
                                mensagens = {
                                    "valor_invalido": "Operação falhou! O valor informado é inválido.",
                                    "saldo_insuficiente": "Operação falhou! Você não tem saldo suficiente.",
                                    "limite_excedido": "Operação falhou! O valor do saque excede o limite.",
                                    "limite_saques_excedido": "Operação falhou! Número máximo de saques excedido."
                                }
                                print(mensagens[resultado])
                    except ValueError:
                        print("Por favor, insira um valor numérico válido.")
                elif opcao_conta == "e":
                    print(conta.emitir_extrato())
                elif opcao_conta == "q":
                    break
        else:
            print("Conta não encontrada.")

    elif opcao_principal == "3":
        banco.listar_contas()

    elif opcao_principal == "4":
        break
