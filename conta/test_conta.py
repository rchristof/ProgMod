import unittest
from conta import *
from user import *
from return_messages import *

contas = []
userTest = {"name": "Pedro", "surname": "Rossi", "cpf": "12345678910", "password": "mariorossi1234"}
contas_test1 = {"CPF": 16557283774, "IBAN": 100000, "balance": 20}

class TestUser(unittest.TestCase):
    def test_01_createNewAccount_1(self):
        print("Test Case 01 - Creating a new account with sucess")
        ret_val = createNewUser(userTest["name"], userTest["surname"], userTest["cpf"], userTest["password"])
        self.assertEqual(ret_val, msg_success)
    def test_02_createNewAccount_2(self):
        print("Test Case 02 - Creating a new account ")
        ret_val = createNewUser(userTest["name"], userTest["surname"], userTest["cpf"], userTest["password"])
        self.assertEqual(ret_val, msg_err_userAlreadyExists)
    def test_03_createNewAccount_3(self):
        print("Test Case 03 - Creating a new account ")
        cpf = "12345678910"
        ret_val = createNewConta(cpf)
        self.assertEqual(ret_val, msg_err_contaAlreadyExists)
    def test_04_verifyExistenceConta_1(self):
        print("Test Case 04 - Verifying Existence Conta with a wrong cpf")
        cpf = "12345"
        ret_val = verifyExistenceConta(cpf)
        self.assertEqual(ret_val, msg_err_invalidCpf)
    def test_05_verifyExistenceConta_2(self):
        print("Test Case 05 - Verifying Existence Conta that not exists")
        cpf = "12345678912"
        ret_val = verifyExistenceConta(cpf)
        self.assertEqual(ret_val, msg_err_contaNotExists)
    def test_06_verifyExistenceConta_3(self):
        print("Test Case 06 - Verifying Existence Conta that exists")
        cpf = "12345678910"
        ret_val = verifyExistenceConta(cpf)
        self.assertEqual(ret_val, msg_success)
    def test_07_verifyBalance_1(self):
        print("Test Case 07 - Verifying Balance with a wrong val")
        cpf = "12345678912"
        iban = "1222222222"
        val = -2
        ret_val = verifyBalance(cpf, iban, val)
        self.assertEqual(ret_val, msg_err_invalidVal)
    def test_08_verifyBalance_2(self):
        print("Test Case 08 - Verifying Balance with a wrong iban")
        cpf = "12345678912"
        iban = 12345678
        val = 100
        ret_val = verifyBalance(cpf, iban, val)
        self.assertEqual(ret_val, msg_err_contaNotExists)
    def test_09_verifyBalance_3(self):
        print("Test Case 09 - Verifying Balance with a wrong iban")
        #falta terminar
    def test_10_getConta_01(self):
        print("Test Case 10 - Verifying getConta with an unexistense conta")
        cpf = "15448759778"
        ret_val = getConta(cpf)
        self.assertEqual(ret_val, msg_err_contaNotExists)
    def test_11_verifyFormatIban_01(self):
        print("Test Case 11 - Verifying format IBAN with a correct format") 
        iban = 12345678
        ret_val = verifyFormatIban(iban)
        self.assertEqual(ret_val, msg_success)
    def test_12_verifyFormatIban_02(self):
        print("Test Case 12 - Verifying format IBAN with a incorrect format (less numbers)") 
        iban = 123456
        ret_val = verifyFormatIban(iban)
        self.assertEqual(ret_val, msg_err_invalidIban)
    def test_13_verifyFormatIban_03(self):
        print("Test Case 13 - Verifying format IBAN with a incorrect format (string)")
        iban = "12345678"
        ret_val = verifyFormatIban(iban)
        self.assertEqual(ret_val, msg_err_invalidIban)
    #def test_14_updateBalance_01(self):


if __name__ == '__main__':
    unittest.main()
