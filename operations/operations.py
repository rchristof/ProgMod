from conta import updateBalance, verifyExistenceConta, verifyBalance  # Funções do módulo Conta
from user import isLoggedIn  # Função do módulo User
from datetime import datetime
from fpdf import FPDF
import platform
import json
import os
from return_messages import *

__all__ = ["makeDeposit", "makeTransfer", "generateReport", "loadTransactionsFromFile", "saveTransactionsToFile"]

_transactions = []

def getTransactions():
    """
    Description: Retrieves a copy of the current transactions list.\n
    Coupling:\n
        Input parameters: none
        Output values:
            - A list of transaction dictionaries currently stored in memory.
    Coupling Conditions:\n
        Entry assertion: none
        Exit assertion:
            - A copy of the transactions list is returned without modifying the original list.
    Restrictions: The returned list is independent of the original and modifications to it do not affect the global `_transactions`.
    """
    return _transactions.copy()


def setTransactions(transactions):
    """
    Description: Replaces the current transactions list with a new one.\n
    Coupling:\n
        Input parameters:
            - transactions -> A list of transaction dictionaries to replace the current list.
        Output values: none
    Coupling Conditions:\n
        Entry assertion:
            - The input must be a valid list of dictionaries formatted as transactions.
        Exit assertion:
            - The global `_transactions` list is replaced with the provided one.
    Restrictions: Assumes the provided list contains valid transaction dictionaries and does not validate its content.
    """

    _transactions.clear()
    _transactions.extend(transactions)


def loadTransactionsFromFile():
    """
    Description: Loads transactions from a file into the memory.\n
    Coupling:\n
        Input parameters: none
        Output values: none
    Coupling Conditions:\n
        Entry assertion:
            - The file should exist at the predefined path and be formatted as a valid JSON list of transactions.
        Exit assertion:
            - The global `_transactions` list is updated with the content of the file.
            - If the file is missing or invalid, `_transactions` is set to an empty list.
    Restrictions:
        - If the file is malformed (not a valid JSON), `_transactions` is cleared.
        - Assumes the file path is correctly defined as `database/transactions/_transactions.txt`.
    """

    file_path="database/transactions/_transactions.txt"
    try:
        with open(file_path, "r") as file:
            transactions = json.load(file)
            setTransactions(transactions)  # Atualiza a lista de transações
    except FileNotFoundError:
        setTransactions([])  # Inicializa a lista como vazia
    except json.JSONDecodeError:
        setTransactions([])


def saveTransactionsToFile():
    """
    Description: Saves the current transactions list to a file.\n
    Coupling:\n
        Input parameters: none
        Output values: none
    Coupling Conditions:\n
        Entry assertion:
            - The global `_transactions` list must be a valid list of transaction dictionaries.
        Exit assertion:
            - The contents of `_transactions` are written to the predefined file path in JSON format.
    Restrictions:
        - The file path is predefined as `database/transactions/_transactions.txt`.
        - Assumes the directory structure exists and is writable.
    """

    file_path="database/transactions/_transactions.txt"
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
        print("\nOperation denied: " + resultIsLoggedIn["message"])
        return resultIsLoggedIn

    # Verifica se o formato do IBAN é válido
    if (isinstance(IBAN, str) == False) or ((len(IBAN) == 8) == False) or (IBAN.isdigit() == False):
        print("\nOperation denied: " + msg_err_invalidIban["message"])
        return msg_err_invalidIban  # Invalid IBAN format

    # Verifica se a conta existe
    resultVerifyExistenceConta = verifyExistenceConta(CPF, IBAN)
    if resultVerifyExistenceConta != msg_success:
        print("\nOperation denied: " + resultVerifyExistenceConta["message"])
        return resultVerifyExistenceConta
    
    # Verifica se o valor é válido
    if (isinstance(val, (int, float)) == False) or val <= 0:
        print("\nOperation denied: " + msg_err_invalidVal["message"])
        return msg_err_invalidVal

    # Atualiza o saldo da conta
    update_result = updateBalance(CPF, IBAN, val)
    if update_result != msg_success:
        print("\nError on balance updating: " + update_result["message"])
        return update_result  # Retorna erro da função updateBalance

    # Transação registrada
    updateTransactions(IBAN, IBAN, val)  # sourceIBAN = destIBAN indica depósito
    print("\nSuccessful deposit")
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
        print("\nOperation denied: " + resultIsLoggedIn["message"])
        return resultIsLoggedIn

    # Verifica se o destCPF é valido
    if len(destCPF) != 11 or destCPF.isdigit() == False:
        print("\nOperation denied: " + msg_err_invalidCpf["message"] + " (destination)")
        return msg_err_invalidCpf

    # Verifica se os CPF sao eguals
    if sourceCPF == destCPF:
        print("\nOperation denied: The source and destination CPFs are the same")
        return msg_err_invalidCpf

    # Verifica se o formato do sourceIBAN é válido
    if (isinstance(sourceIBAN, str) == False) or ((len(sourceIBAN) == 8) == False) or (sourceIBAN.isdigit() == False):
        print("\nOperation denied: " + msg_err_invalidIban["message"] + " (source IBAN)")
        return msg_err_invalidIban  # Invalid sourceIBAN format
    # Verifica se o formato do destIBAN é válido
    if (isinstance(destIBAN, str) == False) or ((len(destIBAN) == 8) == False) or (destIBAN.isdigit() == False):
        print("\nOperation denied: " + msg_err_invalidIban["message"] + " (destination IBAN)")
        return msg_err_invalidIban  # Invalid destIBAN format
    
    # Verifica se os CPF sao eguals
    if sourceIBAN == destIBAN:
        print("\nOperation denied: The source and destination IBANs are the same")
        return msg_err_invalidIban

    # Verifica se o valor é válido
    if (isinstance(val, (int, float)) == False) or val <= 0:
        print("\nOperation denied: " + msg_err_invalidVal["message"])
        return msg_err_invalidVal

    # Verifica se as contas existem
    resultVerifyExistenceConta = verifyExistenceConta(sourceCPF, sourceIBAN)
    if resultVerifyExistenceConta != msg_success:
        print("\nOperation denied: " + resultVerifyExistenceConta["message"] + " (source)")
        return resultVerifyExistenceConta

    resultVerifyExistenceConta = verifyExistenceConta(destCPF, destIBAN)
    if resultVerifyExistenceConta != msg_success:
        print("\nOperation denied: " + resultVerifyExistenceConta["message"] + " (destination)")
        return resultVerifyExistenceConta

    # Verifica se o saldo é suficiente
    resultVerifyBalance = verifyBalance(sourceCPF, sourceIBAN, val)
    if resultVerifyBalance != msg_success:
        print("\nOperation denied: " + resultVerifyBalance["message"])
        return resultVerifyBalance

    # Atualiza o saldo das contas
    withdraw_result = updateBalance(sourceCPF, sourceIBAN, -val)
    if withdraw_result != msg_success:
        print("\nError on balance updating: " + withdraw_result["message"])
        return withdraw_result  # Retorna erro da função updateBalance

    deposit_result = updateBalance(destCPF, destIBAN, val)
    if deposit_result != msg_success:
        print("\nError on balance updating: " + deposit_result["message"])
        return deposit_result  # Retorna erro da função updateBalance

    # Transação registrada
    updateTransactions(sourceIBAN, destIBAN, val)  # sourceIBAN != destIBAN indica transferência
    print("\nSuccessful transfer")
    return msg_success

# Geração e conversão de relatórios
def generateReport(CPF, IBAN):
    """
    Description: Generates a PDF report of transactions for a specific account and optionally converts it to UTF-8 format.\n
    Coupling:\n
        Input parameters:
            - CPF -> The user's CPF (a string with exactly 11 digits).
            - IBAN -> The account's IBAN (a string of exactly 8 numeric digits).
        Output values:
            - None if the report generation is successful.
            - Error messages if any validation or operation fails.
    Coupling Conditions:\n
        Entry assertion:
            - CPF and IBAN must be valid strings in their respective formats.
            - The user must be logged in.
            - The account corresponding to CPF and IBAN must exist.
        Exit assertion:
            - A PDF report is generated containing all transactions related to the IBAN.
            - The file is saved with the naming format `report_{CPF}_{IBAN}_utf32.pdf`.
            - If conversion to UTF-8 fails, no output is returned.
    Restrictions:
        - Requires access to the `FPDF` library and the UTF-32 to UTF-8 converter.
        - Assumes the global `_transactions` list contains valid transaction data.
    """


    # Verifica se o usuário está logado
    resultIsLoggedIn = isLoggedIn(CPF)
    if resultIsLoggedIn != msg_success:
        print("\nOperation denied: " + resultIsLoggedIn["message"])
        return resultIsLoggedIn

    # Verifica se o formato do IBAN é válido
    if (isinstance(IBAN, str) == False) or ((len(IBAN) == 8) == False) or (IBAN.isdigit() == False):
        print("\nOperation denied: " + msg_err_invalidIban["message"])
        return msg_err_invalidIban  # Invalid IBAN format

    # Verifica se a conta existe
    resultVerifyExistenceConta = verifyExistenceConta(CPF, IBAN)
    if resultVerifyExistenceConta != msg_success:
        print("\nOperation denied: " + resultVerifyExistenceConta["message"])
        return resultVerifyExistenceConta

    report = sorted(
        [t for t in _transactions if t["sourceIBAN"] == IBAN or t["destIBAN"] == IBAN],
        key=lambda x: x["date"],
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
        elif t["destIBAN"] == IBAN and t["sourceIBAN"] != IBAN:
            transaction_type = "Received".encode("utf-32").decode("utf-32")
            details = f"Amount: {t['amount']} by {t['sourceIBAN']}".encode("utf-32").decode("utf-32")
        else:
            transaction_type = "Transfer".encode("utf-32").decode("utf-32")
            details = f"Amount: {t['amount']} to {t['destIBAN']}".encode("utf-32").decode("utf-32")

        pdf.cell(200, 10, txt=f"{t['date']} - {transaction_type} - {details}", ln=True, align="L")

    utf32_pdf_file = f"report_{CPF}_{IBAN}_utf32.pdf"
    pdf.output(utf32_pdf_file)
    
    if platform.system() == "Windows":
        conversion_command = f"utils\\conversor\\conv_utf32_utf8.exe {utf32_pdf_file}"
    else:
        conversion_command = f"./utils/conversor/conv_utf32_utf8 {utf32_pdf_file}"

    conversion_result = os.system(conversion_command)

    if conversion_result != 0:
        return
    
    return

def updateTransactions(sourceIBAN, destIBAN, amount):
    """
    Description: Records a new transaction in the transactions list.\n
    Coupling:\n
        Input parameters:
            - sourceIBAN -> The source IBAN involved in the transaction.
            - destIBAN -> The destination IBAN involved in the transaction.
            - amount -> The amount of money transferred or deposited.
        Output values: none
    Coupling Conditions:\n
        Entry assertion:
            - The `sourceIBAN` and `destIBAN` must be valid strings.
            - `amount` must be a positive or negative numerical value.
        Exit assertion:
            - A new transaction dictionary is appended to the global `_transactions` list.
    Restrictions: Does not validate the content of the parameters or check for duplicate transactions.
    """

    transaction = {
        "sourceIBAN": sourceIBAN,
        "destIBAN": destIBAN,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    _transactions.append(transaction)
