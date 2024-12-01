import unittest
from operations import *
from user import *
from conta import *
from return_messages import *

userTest = {"name": "Mario", "surname": "Rossi", "cpf": "12345678910", "password": "mariorossi1234"}
userTest2 = {"name": "Gianni", "surname": "Verdi", "cpf": "22345678910", "password": "giannigianni"}

invalidIban = "1234567"  
validIban = "12345678"   
invalidVal = -100        
validVal = 100

class TestOperations(unittest.TestCase):
    def test_01_makeDeposit_success(self):
        print("Test Case 01 - Make Deposit with success")
        createNewUser(userTest["name"], userTest["surname"], userTest["cpf"], userTest["password"])
        login(userTest["cpf"], userTest["password"])
        ret_val = makeDeposit(userTest["cpf"], getConta(userTest["cpf"])["IBAN"], validVal)
        self.assertEqual(ret_val, msg_success)

    def test_02_makeDeposit_user_not_logged_in(self):
        print("Test Case 02 - Make Deposit when user is not logged in")
        logout(userTest["cpf"])
        ret_val = makeDeposit(userTest["cpf"], getConta(userTest["cpf"])["IBAN"], validVal)
        self.assertEqual(ret_val, msg_err_userNotLoggedIn)

    def test_03_makeDeposit_invalid_iban(self):
        print("Test Case 03 - Make Deposit with invalid IBAN")
        login(userTest["cpf"], userTest["password"])
        ret_val = makeDeposit(userTest["cpf"], invalidIban, validVal)
        self.assertEqual(ret_val, msg_err_invalidIban)

    def test_04_makeDeposit_account_not_exists(self):
        print("Test Case 04 - Make Deposit when account does not exist")
        ret_val = makeDeposit(userTest["cpf"], validIban, validVal)
        self.assertEqual(ret_val, msg_err_contaNotExists)

    def test_05_makeDeposit_invalid_value(self):
        print("Test Case 05 - Make Deposit with invalid value")
        ret_val = makeDeposit(userTest["cpf"], getConta(userTest["cpf"])["IBAN"], invalidVal)
        self.assertEqual(ret_val, msg_err_invalidVal)

    def test_06_makeTransfer_success(self):
        print("Test Case 06 - Make Transfer with success")
        createNewUser(userTest2["name"], userTest2["surname"], userTest2["cpf"], userTest2["password"])
        ret_val = makeTransfer(userTest["cpf"], userTest2["cpf"], getConta(userTest["cpf"])["IBAN"], getConta(userTest2["cpf"])["IBAN"], 50)
        self.assertEqual(ret_val, msg_success)

    def test_07_makeTransfer_user_not_logged_in(self):
        print("Test Case 07 - Make Transfer when user is not logged in")
        logout(userTest["cpf"])
        ret_val = makeTransfer(userTest["cpf"], userTest2["cpf"], getConta(userTest["cpf"])["IBAN"], getConta(userTest2["cpf"])["IBAN"], 50)
        self.assertEqual(ret_val, msg_err_userNotLoggedIn)

    def test_08_makeTransfer_invalid_destCPF(self):
        print("Test Case 08 - Make Transfer with invalid destination CPF")
        login(userTest["cpf"], userTest["password"])
        ret_val = makeTransfer(userTest["cpf"], "fake_value", getConta(userTest["cpf"])["IBAN"], getConta(userTest2["cpf"])["IBAN"], 50)
        self.assertEqual(ret_val, msg_err_invalidCpf)

    def test_09_makeTransfer_same_source_dest_CPF(self):
        print("Test Case 09 - Make Transfer with same source and destination CPF")
        ret_val = makeTransfer(userTest["cpf"], userTest["cpf"], getConta(userTest["cpf"])["IBAN"], getConta(userTest2["cpf"])["IBAN"], 50)
        self.assertEqual(ret_val, msg_err_invalidCpf)

    def test_10_makeTransfer_invalid_source_IBAN(self):
        print("Test Case 10 - Make Transfer with invalid source IBAN")
        ret_val = makeTransfer(userTest["cpf"], userTest2["cpf"], "invalid_iban", getConta(userTest2["cpf"])["IBAN"], 50)
        self.assertEqual(ret_val, msg_err_invalidIban)

    def test_11_makeTransfer_same_IBANs(self):
        print("Test Case 11 - Make Transfer with same source and destination IBAN")
        ret_val = makeTransfer(userTest["cpf"], userTest2["cpf"], getConta(userTest["cpf"])["IBAN"], getConta(userTest["cpf"])["IBAN"], 50)
        self.assertEqual(ret_val, msg_err_invalidIban)

    def test_12_makeTransfer_insufficient_balance(self):
        print("Test Case 12 - Make Transfer with insufficient balance")
        ret_val = makeTransfer(userTest["cpf"], userTest2["cpf"], getConta(userTest["cpf"])["IBAN"], getConta(userTest2["cpf"])["IBAN"], 70)
        self.assertEqual(ret_val, msg_err_insufficientBal)

    def test_13_makeTransfer_invalid_value(self):
        print("Test Case 13 - Make Transfer with invalid value")
        ret_val = makeTransfer(userTest["cpf"], userTest2["cpf"], getConta(userTest["cpf"])["IBAN"], getConta(userTest2["cpf"])["IBAN"], "invalid_val")
        self.assertEqual(ret_val, msg_err_invalidVal)

    def test_14_generateReport_success(self):
        print("Test Case 14 - Generate Report with success")
        ret_val = generateReport(userTest["cpf"], getConta(userTest["cpf"])["IBAN"])
        self.assertEqual(ret_val, None)

    def test_15_saveTransactionsToFile(self):
        print("Test Case 15 - Save Transactions To File")
        ret_val = saveTransactionsToFile()
        self.assertEqual(ret_val, None)

unittest.main()

'''
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
'''
