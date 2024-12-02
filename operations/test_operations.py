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

    """APAGAR ESSES TESTES DEPOIS"""
    def test_14_generateReport_success(self):
        print("Test Case 14 - Generate Report with success")
        ret_val = generateReport(userTest["cpf"], getConta(userTest["cpf"])["IBAN"])
        self.assertEqual(ret_val, None)

    def test_15_saveTransactionsToFile_success(self):
        print("Test Case 15 - Save Transactions To File with success")
        ret_val = saveTransactionsToFile(userTest["cpf"])
        self.assertEqual(ret_val, None)

        setTransactions([]) #apagar
        ret_val = getTransactions()
        print(ret_val)

    def test_16_loadTransactionsFromFile_success(self):
        print("Test Case 16 - Load Transactions From File with success")
        ret_val = loadTransactionsFromFile(userTest["cpf"])
        self.assertEqual(ret_val, None)
    
    def test_17_getTransactions_success(self):
        print("Test Case 17 - Get Transactions with success")
        ret_val = getTransactions()
        print(ret_val)


unittest.main()