from user import *
from return_messages import *
import random

__all__ = ["updateBalance", "verifyExistenceConta", "createNewConta"]

contas = []

def verifyFormatIban(IBAN):
    if isinstance(IBAN, str) and len(IBAN) == 8 and IBAN.isdigit():
        return msg_success  # Success
    return msg_err_invalidIban  # Invalid IBAN format

def createNewConta(CPF):
    # Verifica se o usuário existe
    if not verifyExistenceUser(CPF):
        return msg_err_userNotExists  # User not exists
    
    # Verifica se já existe uma conta para o CPF
    if verifyExistenceConta(CPF):
        return msg_err_contaNotExists  # Conta not exists

    # Criação do número IBAN de forma aleatória
    iban = str(random.randint(10000000, 99999999)) 

    contas.append({"CPF": CPF, "IBAN": iban, "balance": 0})

    return msg_success  # Success

def updateBalance(CPF, IBAN, val):
    # Verifica o formato do IBAN
    format_check = verifyFormatIban(IBAN)
    if format_check["code"] != 0:
        return format_check  # Return error message from verifyFormatIban

    # Verifica se o valor é válido (diferente de zero)
    if not isinstance(val, (int, float)) or val == 0:
        return msg_err_invalidVal  # Invalid val

    # Encontra a conta correspondente
    for conta in contas:
        if conta['CPF'] == CPF and conta['IBAN'] == IBAN:
            if conta['balance'] + val < 0:
                return msg_err_insufficientBal  # Insufficient balance
            conta['balance'] += val
            return msg_success  # Success

    return msg_err_contaNotExists  # Conta not exists

def verifyExistenceConta(CPF, IBAN=None):
    for conta in contas:
        if conta['CPF'] == CPF:
            if IBAN is None or conta['IBAN'] == IBAN:
                return msg_success  # Success
    return msg_err_contaNotExists  # Conta not exists

def verifyBalance(CPF, IBAN, val):
    # Verifica se o valor é válido (positivo)
    if not isinstance(val, (int, float)) or val <= 0:
        return msg_err_invalidVal  # Invalid val

    # Encontra a conta correspondente
    for conta in contas:
        if conta['CPF'] == CPF and conta['IBAN'] == IBAN:
            if conta['balance'] >= val:
                return msg_success  # Success
            return msg_err_insufficientBal  # Insufficient balance

    return msg_err_contaNotExists   # Conta not exists
