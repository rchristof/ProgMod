import json
import os
from datetime import datetime
from fpdf import FPDF
import platform

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


# Gerenciamento de transações
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


# Operações bancárias
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


def updateTransactions(sourceIBAN, destIBAN, amount):
    """Adiciona uma nova transação à lista."""
    transaction = {
        "sourceIBAN": sourceIBAN,
        "destIBAN": destIBAN,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    _transactions.append(transaction)


# Geração e conversão de relatórios
def generateReport(CPF, IBAN):
    """Gera um relatório de transações no formato PDF (UTF-32) e converte para UTF-8."""
    # Filtra transações
    report = sorted(
        [t for t in _transactions if t["sourceIBAN"] == IBAN or t["destIBAN"] == IBAN],
        key=lambda x: x["date"],
    )

    # Gera o PDF em UTF-32
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

    # Determina o comando de conversão com base no sistema operacional
    
    if platform.system() == "Windows":
        conversion_command = f"utils\\conversor\\conv_utf32_utf8.exe {utf32_pdf_file}"
    else:
        conversion_command = f"./utils/conversor/conv_utf32_utf8 {utf32_pdf_file}"

    # Executa o comando
    conversion_result = os.system(conversion_command)

    if conversion_result != 0:
        return

    # Retorna o arquivo convertido
    return
