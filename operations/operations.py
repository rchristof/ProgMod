from conta import updateBalance, verifyExistenceConta, verifyBalance  # Funções do módulo Conta
from user import isLoggedIn  # Função do módulo User
from datetime import datetime
from fpdf import FPDF

__all__ = ["makeDeposit", "makeTransfer", "generateReport"]

transactions = []

def makeDeposit(CPF, IBAN, val):
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
    updateTransactions(IBAN, IBAN, val)  # sourceIBAN = destIBAN indica depósito
    return {"code": 0, "message": "Deposit successful"}

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
    # Verifica se o usuário está logado
    if isLoggedIn(CPF) != 0:
        return {"code": 1, "message": "User not logged in"}

    # Verifica se a conta existe
    if verifyExistenceConta(CPF, IBAN) != 0:
        return {"code": 2, "message": "Conta not exists"}

    # Filtra as transações do IBAN e organiza por data
    report = sorted(
        [t for t in transactions if t["sourceIBAN"] == IBAN or t["destIBAN"] == IBAN],
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
