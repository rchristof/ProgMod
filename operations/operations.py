from conta import updateBalance, verifyExistenceConta, verifyBalance  # Funções do módulo Conta
from user import isLoggedIn  # Função do módulo User
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


def makeDeposit(CPF, IBAN, val):
    """
        Description: Implements Deposit functionality.\n
        Coupling:\n
            Input parameters:
                CPF -> User's CPF (a string with exactly 11 digits)
                IBAN -> Account IBAN (a string with exactly 8 digits)
                val -> Deposit value (a positive integer or float)
            Output values:
                msg_err_userNotLoggedIn -> If the user is not logged in
                msg_err_invalidIban -> If the IBAN format is invalid
                msg_err_contaNotExists -> If the account does not exist
                msg_err_invalidVal -> If the deposit value is invalid (e.g., negative or zero)
                msg_success -> If the deposit operation is successful
        Coupling Conditions:\n
            Entry assertion: none
            Exit assertion:
                msg_success -> The account balance is updated and the transaction is recorded
                Other cases -> No changes to the account balance or transactions
    """

    # Verifica se o usuário está logado
    resultIsLoggedIn = isLoggedIn(CPF)
    if resultIsLoggedIn != msg_success:
        print("Operation denied: " + resultIsLoggedIn["message"])
        return resultIsLoggedIn

    # Verifica se o formato do IBAN é válido
    if (isinstance(IBAN, str) == False) or ((len(IBAN) == 8) == False) or (IBAN.isdigit() == False):
        print("Operation denied: " + msg_err_invalidIban["message"])
        return msg_err_invalidIban  # Invalid IBAN format

    # Verifica se a conta existe
    resultVerifyExistenceConta = verifyExistenceConta(CPF, IBAN)
    if resultVerifyExistenceConta != msg_success:
        print("Operation denied: " + resultVerifyExistenceConta["message"])
        return resultVerifyExistenceConta
    
    # Verifica se o valor é válido
    if (isinstance(val, (int, float)) == False) or val <= 0:
        print("Operation denied: " + msg_err_invalidVal["message"])
        return msg_err_invalidVal

    # Atualiza o saldo da conta
    update_result = updateBalance(CPF, IBAN, val)
    if update_result != msg_success:
        print("Error on balance updating: " + update_result["message"])
        return update_result  # Retorna erro da função updateBalance

    # Transação registrada
    updateTransactions(IBAN, IBAN, val)  # sourceIBAN = destIBAN indica depósito
    print("Successful deposit")
    return msg_success

def makeTransfer(sourceCPF, destCPF, sourceIBAN, destIBAN, val):
    """
        Description: Implements Transfer functionality between two accounts.\n
        Coupling:\n
            Input parameters:
                sourceCPF -> Source user's CPF (a string with exactly 11 digits)
                destCPF -> Destination user's CPF (a string with exactly 11 digits)
                sourceIBAN -> Source account IBAN (a string with exactly 8 digits)
                destIBAN -> Destination account IBAN (a string with exactly 8 digits)
                val -> Transfer value (a positive integer or float)
            Output values:
                msg_err_userNotLoggedIn -> If the source user is not logged in
                msg_err_invalidCpf -> If the source or destination CPF is invalid, or if the source and destination CPFs are the same
                msg_err_invalidIban -> If the source or destination IBAN is invalid, or if the source and destination IBANs are the same
                msg_err_invalidVal -> If the transfer value is invalid (e.g., negative or zero)
                msg_err_contaNotExists -> If the source or destination account does not exist
                msg_err_insufficientBalance -> If the source account has insufficient balance
                msg_success -> If the transfer operation is successful
        Coupling Conditions:\n
            Entry assertion: none
            Exit assertion:
                msg_success -> The source account balance is reduced, the destination account balance is increased, and the transaction is recorded
                Other cases -> No changes to the account balances or transactions
    """
    
    # Verifica se o usuário está logado
    resultIsLoggedIn = isLoggedIn(sourceCPF)
    if resultIsLoggedIn != msg_success:
        print("Operation denied: " + resultIsLoggedIn["message"])
        return resultIsLoggedIn

    # Verifica se o destCPF é valido
    if len(destCPF) != 11 or destCPF.isdigit() == False:
        print("Operation denied: " + msg_err_invalidCpf["message"] + " (destination)")
        return msg_err_invalidCpf

    # Verifica se os CPF sao eguals
    if sourceCPF == destCPF:
        print("Operation denied: The source and destination CPFs are the same")
        return msg_err_invalidCpf

    # Verifica se o formato do sourceIBAN é válido
    if (isinstance(sourceIBAN, str) == False) or ((len(sourceIBAN) == 8) == False) or (sourceIBAN.isdigit() == False):
        print("Operation denied: " + msg_err_invalidIban["message"] + " (source IBAN)")
        return msg_err_invalidIban  # Invalid sourceIBAN format
    # Verifica se o formato do destIBAN é válido
    if (isinstance(destIBAN, str) == False) or ((len(destIBAN) == 8) == False) or (destIBAN.isdigit() == False):
        print("Operation denied: " + msg_err_invalidIban["message"] + " (destination IBAN)")
        return msg_err_invalidIban  # Invalid destIBAN format
    
    # Verifica se os CPF sao eguals
    if sourceIBAN == destIBAN:
        print("Operation denied: The source and destination IBANs are the same")
        return msg_err_invalidIban

    # Verifica se o valor é válido
    if (isinstance(val, (int, float)) == False) or val <= 0:
        print("Operation denied: " + msg_err_invalidVal["message"])
        return msg_err_invalidVal

    # Verifica se as contas existem
    resultVerifyExistenceConta = verifyExistenceConta(sourceCPF, sourceIBAN)
    if resultVerifyExistenceConta != msg_success:
        print("Operation denied: " + resultVerifyExistenceConta["message"] + " (source)")
        return resultVerifyExistenceConta

    resultVerifyExistenceConta = verifyExistenceConta(destCPF, destIBAN)
    if resultVerifyExistenceConta != msg_success:
        print("Operation denied: " + resultVerifyExistenceConta["message"] + " (destination)")
        return resultVerifyExistenceConta

    # Verifica se o saldo é suficiente
    resultVerifyBalance = verifyBalance(sourceCPF, sourceIBAN, val)
    if resultVerifyBalance != msg_success:
        print("Operation denied: " + resultVerifyBalance["message"])
        return resultVerifyBalance

    # Atualiza o saldo das contas
    withdraw_result = updateBalance(sourceCPF, sourceIBAN, -val)
    if withdraw_result != msg_success:
        print("Error on balance updating: " + withdraw_result["message"])
        return withdraw_result  # Retorna erro da função updateBalance

    deposit_result = updateBalance(destCPF, destIBAN, val)
    if deposit_result != msg_success:
        print("Error on balance updating: " + deposit_result["message"])
        return deposit_result  # Retorna erro da função updateBalance

    # Transação registrada
    updateTransactions(sourceIBAN, destIBAN, val)  # sourceIBAN != destIBAN indica transferência
    print("Successful transfer")
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
