from user import verifyExistenceUser
import random

contas = []

def verifyFormatIban(IBAN):
    if isinstance(IBAN, str) and len(IBAN) == 8 and IBAN.isdigit():
        return 0  # Success
    return 4  # Invalid IBAN format

def createNewConta(CPF):
    # Verifica se o usuário existe
    if not verifyExistenceUser(CPF):
        return {"code": 3, "message": "User not exists"} 
    
    # Verifica se já existe uma conta para o CPF -- talvez falte algo
    if verifyExistenceConta(CPF):
        return {"code": 2, "message": "Conta already exists"}

    # Criação do número IBAN de forma aleatória
    iban = str(random.randint(10000000, 99999999)) 

    contas.append({"CPF": CPF, "IBAN": iban, "balance": 0})

    return {"code": 0, "message": "Account created successfully"}

# Atualiza o saldo de uma conta
def updateBalance(CPF, IBAN, val):
    # Verifica o formato do IBAN
    if verifyFormatIban(IBAN) != 0:
        return {"code": 4, "message": "Invalid IBAN format"}

    # Verifica se o valor é válido (diferente de zero)
    if not isinstance(val, (int, float)) or val == 0:
        return {"code": 5, "message": "Invalid val"}

    # Encontra a conta correspondente
    for conta in contas:
        if conta['CPF'] == CPF and conta['IBAN'] == IBAN:
            if conta['balance'] + val < 0:
                return {"code": 6, "message": "Insufficient balance"}
            conta['balance'] += val
            return {"code": 0, "message": "Balance updated successfully", "new_balance": conta['balance']}

    return {"code": 2, "message": "Conta not exists"}

# Verifica se uma conta existe
def verifyExistenceConta(CPF, IBAN=None):
    for conta in contas:
        if conta['CPF'] == CPF:
            if IBAN is None or conta['IBAN'] == IBAN:
                return 0  # Success
    return 2  # Conta not exists

# Verifica o saldo disponível de uma conta
def verifyBalance(CPF, IBAN, val):
    # Verifica se o valor é válido (positivo)
    if not isinstance(val, (int, float)) or val <= 0:
        return 5  # Invalid val

    # Encontra a conta correspondente
    for conta in contas:
        if conta['CPF'] == CPF and conta['IBAN'] == IBAN:
            if conta['balance'] >= val:
                return 0  # Success
            return 6  # Insufficient balance

    return 2  # Conta not exists
