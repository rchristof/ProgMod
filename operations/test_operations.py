import json
from datetime import datetime
from fpdf import FPDF

__all__ = [
    "makeDeposit",
    "makeTransfer",
    "generateReport",
    "loadTransactionsFromFile",
    "saveTransactionsToFile",
    "getTransactions",
]

# Lista de transações (privada por convenção)
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
    """Registra um depósito."""
    if val <= 0:
        return {"code": 5, "message": "Invalid val"}

    updateTransactions(IBAN, IBAN, val)  # sourceIBAN = destIBAN indica depósito
    return {"code": 0, "message": "Deposit successful"}


def makeTransfer(sourceCPF, destCPF, sourceIBAN, destIBAN, val):
    """Registra uma transferência."""
    updateTransactions(sourceIBAN, destIBAN, val)
    return {"code": 0, "message": "Transfer successful"}


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
    return {"code": 0, "message": "Report generated successfully", "file": file_name}


def updateTransactions(sourceIBAN, destIBAN, amount):
    """Adiciona uma nova transação à lista."""
    transaction = {
        "sourceIBAN": sourceIBAN,
        "destIBAN": destIBAN,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    _transactions.append(transaction)
