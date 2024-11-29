#from conta import updateBalance, verifyExistenceConta, verifyBalance  # Funções do módulo Conta
#from user import isLoggedIn  # Função do módulo User
from datetime import datetime
#from fpdf import FPDF
import os
from return_messages import *

__all__ = ["makeDeposit", "makeTransfer", "generateReport"]

transactions = []

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
    if isLoggedIn(sourceCPF) != 0:
        return {"code": 1, "message": "User not logged in"}

    # Verifica se as contas existem
    if verifyExistenceConta(sourceCPF, sourceIBAN) != 0:
        return {"code": 2, "message": "Source conta not exists"}
    if verifyExistenceConta(destCPF, destIBAN) != 0:
        return {"code": 2, "message": "Destination conta not exists"}

    # Verifica se o saldo é suficiente
    if verifyBalance(sourceCPF, sourceIBAN, val) != 0:
        return {"code": 6, "message": "Insufficient balance"}

    # Atualiza o saldo das contas
    withdraw_result = updateBalance(sourceCPF, sourceIBAN, -val)
    if withdraw_result["code"] != 0:
        return withdraw_result  # Retorna erro da função updateBalance

    deposit_result = updateBalance(destCPF, destIBAN, val)
    if deposit_result["code"] != 0:
        return deposit_result  # Retorna erro da função updateBalance

    # Transação registrada
    updateTransactions(sourceIBAN, destIBAN, val)  # sourceIBAN != destIBAN indica transferência
    return {"code": 0, "message": "Transfer successful"}

def generateReport(CPF, IBAN):
    report = sorted(
        [t for t in transactions if t["sourceIBAN"] == IBAN or t["destIBAN"] == IBAN],
        key=lambda x: x["date"]
    )

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Transaction Report".encode("utf-32").decode("utf-32"), ln=True, align="C")
    pdf.cell(200, 10, txt=f"IBAN: {IBAN}".encode("utf-32").decode("utf-32"), ln=True, align="L")
    pdf.cell(200, 10, txt="Generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ln=True, align="L")
    pdf.ln(10)

    for t in report:
        if t["sourceIBAN"] == t["destIBAN"]:
            transaction_type = "Deposit".encode("utf-32").decode("utf-32")
            details = f"Amount: {t['amount']}".encode("utf-32").decode("utf-32")
        else:
            transaction_type = "Transfer".encode("utf-32").decode("utf-32")
            details = f"Amount: {t['amount']} to {t['destIBAN']}".encode("utf-32").decode("utf-32")

        pdf.cell(200, 10, txt=f"{t['date']} - {transaction_type} - {details}", ln=True, align="L")

    utf32_pdf_file = f"report_{CPF}_{IBAN}_utf32.pdf"
    pdf.output(utf32_pdf_file)

    conversion_command = f"utils\\conversor\\conv_utf32_utf8.exe {utf32_pdf_file}"
    conversion_result = os.system(conversion_command)

    if conversion_result != 0:
        return {"code": 3, "message": "Error converting PDF from UTF-32 to UTF-8"}

    utf8_pdf_file = utf32_pdf_file.replace("_utf32", "_utf8")

    return {"code": 0, "message": "Report generated and converted successfully", "utf8_file": utf8_pdf_file}

def updateTransactions(sourceIBAN, destIBAN, amount):
    # Registra uma nova transação
    transaction = {
        "sourceIBAN": sourceIBAN,
        "destIBAN": destIBAN,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    transactions.append(transaction)


"""
class Operations:
    def __init__(self):
        self.transactions = []

    def makeDeposit(self, CPF, IBAN, val):
        # Verifica se o usuário está logado
        if isLoggedIn(CPF) != 0:
            return {"code": 1, "message": "User not logged in"}

        # Verifica se a conta existe
        if verifyExistenceConta(CPF, IBAN) != 0:
            return {"code": 2, "message": "Conta not exists"}

        # Verifica se o valor é válido
        if val <= 0:
            return {"code": 5, "message": "Invalid val"}

        # Atualiza o saldo da conta
        update_result = updateBalance(CPF, IBAN, val)
        if update_result["code"] != 0:
            return update_result  # Retorna erro da função updateBalance

        # Transação registrada
        self.updateTransactions(IBAN, IBAN, val)  # sourceIBAN = destIBAN indica depósito
        return {"code": 0, "message": "Deposit successful"}

    def makeTransfer(self, sourceCPF, destCPF, sourceIBAN, destIBAN, val):
        # Verifica se o usuário está logado
        if isLoggedIn(sourceCPF) != 0:
            return {"code": 1, "message": "User not logged in"}

        # Verifica se as contas existem
        if verifyExistenceConta(sourceCPF, sourceIBAN) != 0:
            return {"code": 2, "message": "Source conta not exists"}
        if verifyExistenceConta(destCPF, destIBAN) != 0:
            return {"code": 2, "message": "Destination conta not exists"}

        # Verifica se o saldo é suficiente
        if verifyBalance(sourceCPF, sourceIBAN, val) != 0:
            return {"code": 6, "message": "Insufficient balance"}

        # Atualiza o saldo das contas
        withdraw_result = updateBalance(sourceCPF, sourceIBAN, -val)
        if withdraw_result["code"] != 0:
            return withdraw_result  # Retorna erro da função updateBalance

        deposit_result = updateBalance(destCPF, destIBAN, val)
        if deposit_result["code"] != 0:
            return deposit_result  # Retorna erro da função updateBalance

        # Transação registrada
        self.updateTransactions(sourceIBAN, destIBAN, val)  # sourceIBAN != destIBAN indica transferência
        return {"code": 0, "message": "Transfer successful"}

    def generateReport(self, CPF, IBAN):
        # Verifica se o usuário está logado
        if isLoggedIn(CPF) != 0:
            return {"code": 1, "message": "User not logged in"}

        # Verifica se a conta existe
        if verifyExistenceConta(CPF, IBAN) != 0:
            return {"code": 2, "message": "Conta not exists"}

        # Filtra as transações do IBAN e organiza por data
        report = sorted(
            [t for t in self.transactions if t["sourceIBAN"] == IBAN or t["destIBAN"] == IBAN],
            key=lambda x: x["date"]
        )

        # Gera o PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Transaction Report", ln=True, align="C")
        pdf.cell(200, 10, txt=f"IBAN: {IBAN}", ln=True, align="L")
        pdf.cell(200, 10, txt="Generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ln=True, align="L")
        pdf.ln(10)

        # Adiciona transações ao PDF
        for t in report:
            if t["sourceIBAN"] == t["destIBAN"]:
                transaction_type = "Deposit"
                details = f"Amount: {t['amount']}"
            else:
                transaction_type = "Transfer"
                details = f"Amount: {t['amount']} to {t['destIBAN']}"

            pdf.cell(200, 10, txt=f"{t['date']} - {transaction_type} - {details}", ln=True, align="L")

        # Salva o PDF
        file_name = f"report_{CPF}_{IBAN}.pdf"
        pdf.output(file_name)
        return {"code": 0, "message": "Report generated", "file": file_name}

    def updateTransactions(self, sourceIBAN, destIBAN, amount):
        # Registra uma nova transação
        transaction = {
            "sourceIBAN": sourceIBAN,
            "destIBAN": destIBAN,
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.transactions.append(transaction)
"""
