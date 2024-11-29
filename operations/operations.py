#from conta import updateBalance, verifyExistenceConta, verifyBalance  # Funções do módulo Conta
#from user import isLoggedIn  # Função do módulo User
from datetime import datetime
from fpdf import FPDF
import json
import os
from return_messages import *

__all__ = ["makeDeposit", "makeTransfer", "generateReport"]

_transactions = []

def getTransactions():
    """Retorna uma cópia da lista de transações."""
    return _transactions.copy()


def setTransactions(transactions):
    """Substitui a lista de transações."""
    _transactions.clear()
    _transactions.extend(transactions)


def loadTransactionsFromFile(file_path="transactions.txt"):
    """Lê as transações de um arquivo e preenche a lista."""
    try:
        with open(file_path, "r") as file:
            transactions = json.load(file)
            setTransactions(transactions)  # Atualiza a lista de transações
    except FileNotFoundError:
        print(f"Arquivo {file_path} não encontrado. Inicializando lista vazia.")
        setTransactions([])  # Inicializa a lista como vazia
    except json.JSONDecodeError:
        print("Erro ao decodificar o arquivo de transações. Inicializando lista vazia.")
        setTransactions([])


def saveTransactionsToFile(file_path="transactions.txt"):
    """Sobrescreve o arquivo com as transações atuais da lista."""
    with open(file_path, "w") as file:
        json.dump(getTransactions(), file, indent=4)  # Obtém a lista atual

##### Functions for testing the code #####

loggedUserCPF = "12345678901"

def isLoggedIn(cpf):
    if len(cpf) != 11 or cpf.isdigit() == False:
        return msg_err_invalidCpf
    if loggedUserCPF == cpf:
        return msg_success
    else:
        return msg_err_userNotLoggedIn

def verifyExistenceConta(cpf, iban):
    return msg_success

def updateBalance(cpf, iban, val):
    return msg_success

def verifyBalance(cpf, iban, val):
    return msg_success

############################################


def makeDeposit(CPF, IBAN, val):
    # Verifica se o usuário está logado
    resultIsLoggedIn = isLoggedIn(CPF)
    if resultIsLoggedIn != msg_success:
        return resultIsLoggedIn

    # Verifica se o formato do IBAN é válido
    if (isinstance(IBAN, str) == False) or ((len(IBAN) == 8) == False) or (IBAN.isdigit() == False):
        return msg_err_invalidIbanFormat  # Invalid IBAN format
    
    # Verifica se a conta existe
    resultVerifyExistenceConta = verifyExistenceConta(CPF, IBAN)
    if resultVerifyExistenceConta != msg_success:
        return resultVerifyExistenceConta

    # Verifica se o valor é válido
    if (isinstance(val, (int, float)) == False) or val <= 0:
        return msg_err_invalidVal

    # Atualiza o saldo da conta
    update_result = updateBalance(CPF, IBAN, val)
    if update_result != msg_success:
        return update_result  # Retorna erro da função updateBalance

    # Transação registrada
    updateTransactions(IBAN, IBAN, val)  # sourceIBAN = destIBAN indica depósito
    return msg_success


def makeTransfer(sourceCPF, destCPF, sourceIBAN, destIBAN, val):
    
    # Verifica se o usuário está logado
    resultIsLoggedIn = isLoggedIn(sourceCPF)
    if resultIsLoggedIn != msg_success:
        return resultIsLoggedIn

    # Verifica se o destCPF é valido
    if len(destCPF) != 11 or destCPF.isdigit() == False:
        return msg_err_invalidCpf

    # Verifica se os CPF sao eguals
    if sourceCPF == destCPF:
        return msg_err_invalidCpf

    # Verifica se o formato do sourceIBAN é válido
    if (isinstance(sourceIBAN, str) == False) or ((len(sourceIBAN) == 8) == False) or (sourceIBAN.isdigit() == False):
        return msg_err_invalidIban  # Invalid sourceIBAN format
    # Verifica se o formato do destIBAN é válido
    if (isinstance(destIBAN, str) == False) or ((len(destIBAN) == 8) == False) or (destIBAN.isdigit() == False):
        return msg_err_invalidIban  # Invalid destIBAN format
    
    # Verifica se os CPF sao eguals
    if sourceIBAN == destIBAN:
        return msg_err_invalidIban

    # Verifica se o valor é válido
    if (isinstance(val, (int, float)) == False) or val <= 0:
        return msg_err_invalidVal

    # Verifica se as contas existem
    resultVerifyExistenceConta = verifyExistenceConta(sourceCPF, sourceIBAN)
    if resultVerifyExistenceConta != msg_success:
        return resultVerifyExistenceConta

    resultVerifyExistenceConta = verifyExistenceConta(destCPF, destIBAN)
    if resultVerifyExistenceConta != msg_success:
        return resultVerifyExistenceConta

    # Verifica se o saldo é suficiente
    resultVerifyBalance = verifyBalance(sourceCPF, sourceIBAN, val)
    if resultVerifyBalance != msg_success:
        return resultVerifyBalance

    # Atualiza o saldo das contas
    withdraw_result = updateBalance(sourceCPF, sourceIBAN, -val)
    if withdraw_result != msg_success:
        return withdraw_result  # Retorna erro da função updateBalance

    deposit_result = updateBalance(destCPF, destIBAN, val)
    if deposit_result != msg_success:
        return deposit_result  # Retorna erro da função updateBalance

    # Transação registrada
    updateTransactions(sourceIBAN, destIBAN, val)  # sourceIBAN != destIBAN indica transferência
    return msg_success

def generateReport(CPF, IBAN):
    """Gera um relatório em PDF para as transações de um IBAN."""
    report = sorted(
        [t for t in _transactions if t["sourceIBAN"] == IBAN or t["destIBAN"] == IBAN],
        key=lambda x: x["date"],
    )

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Transaction Report", ln=True, align="C")
    pdf.cell(200, 10, txt=f"IBAN: {IBAN}", ln=True, align="L")
    pdf.cell(200, 10, txt="Generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ln=True, align="L")
    pdf.ln(10)

    for t in report:
        transaction_type = "Deposit" if t["sourceIBAN"] == t["destIBAN"] else "Transfer"
        details = (
            f"Amount: {t['amount']}"
            if t["sourceIBAN"] == t["destIBAN"]
            else f"Amount: {t['amount']} to {t['destIBAN']}"
        )
        pdf.cell(200, 10, txt=f"{t['date']} - {transaction_type} - {details}", ln=True, align="L")

    file_name = f"report_{CPF}_{IBAN}.pdf"
    pdf.output(file_name)
    return

def updateTransactions(sourceIBAN, destIBAN, amount):
    """Adiciona uma nova transação à lista."""
    transaction = {
        "sourceIBAN": sourceIBAN,
        "destIBAN": destIBAN,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    _transactions.append(transaction)
