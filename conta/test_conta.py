import unittest
from conta import *
from .conta import verifyFormatIban
from user import *
from return_messages import *

contas = []
userTest = {"name": "Pedro", "surname": "Rossi", "cpf": "12345678910", "password": "mariorossi1234"}
userTest2 = {"name": "Vinicius", "surname": "Amaral", "cpf": "48775489747", "password": "mkjiooac123"}

class TestConta(unittest.TestCase):
    def test_01_createNewAccount_1(self):
        print("Test Case 01 - Creating a new account with success")
        ret_val = createNewUser(userTest["name"], userTest["surname"], userTest["cpf"], userTest["password"])
        self.assertEqual(ret_val, msg_success)

    def test_02_createNewAccount_2(self):
        print("Test Case 02 - Creating a new user that already exists ")
        ret_val = createNewUser(userTest["name"], userTest["surname"], userTest["cpf"], userTest["password"])
        self.assertEqual(ret_val, msg_err_userAlreadyExists)

    def test_03_createNewAccount_3(self):
        print("Test Case 03 - Creating a new account that already exists ")
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
        cpf = "12345678910"
        conta = getConta(cpf)
        iban = conta["IBAN"]
        updateBalance(cpf, iban, 1)
        ret_val = verifyBalance(cpf, iban, 1)
        self.assertEqual(ret_val, msg_success)
    
    def test_10_verifyBalance_4(self):
        print("Test Case 10 - Verifying Balance with insufficient balance")
        cpf = "12345678910"
        conta = getConta(cpf)
        iban = conta["IBAN"]
        val = 500
        ret_val = verifyBalance(cpf, iban, val)
        self.assertEqual(ret_val, msg_err_insufficientBal)
        
    def test_11_getConta_01(self):
        print("Test Case 11 - Verifying getConta with an unexistense conta")
        cpf = "15448759778"
        ret_val = getConta(cpf)
        self.assertEqual(ret_val, msg_err_contaNotExists)

    def teste_12_getConta_02(self):
        print("Test Case 12 - Verifying getConta getting a conta")
        cpf = "12345678910"
        ret_val = getConta(cpf)
        iban = ret_val["IBAN"]
        conta = {'CPF': '12345678910', 'IBAN': iban, 'balance': 1}
        self.assertEqual(ret_val, conta)

    def test_13_verifyFormatIban_01(self):
        print("Test Case 13 - Verifying format IBAN with a correct format") 
        iban = "12345678"
        ret_val = verifyFormatIban(iban)
        self.assertEqual(ret_val, msg_success)

    def test_14_verifyFormatIban_02(self):
        print("Test Case 14 - Verifying format IBAN with a incorrect format (less numbers)") 
        iban = "123456"
        ret_val = verifyFormatIban(iban)
        self.assertEqual(ret_val, msg_err_invalidIban)

    def test_15_verifyFormatIban_03(self):
        print("Test Case 15 - Verifying format IBAN with a incorrect format (int number)")
        iban = 12345678
        ret_val = verifyFormatIban(iban)
        self.assertEqual(ret_val, msg_err_invalidIban)

    def test_16_updateBalance_01(self):
        print("Test Case 16 - Updating balance with an invalid val")
        cpf = "12345678910"
        conta = getConta(cpf)
        iban = conta["IBAN"]
        val = -2
        ret_val = updateBalance(cpf, iban, val)
        self.assertEqual(ret_val, msg_err_insufficientBal)

    def test_17_updateBalance_02(self):
        print("Test Case 17 - Updating balance with an incorret account")
        cpf = "12345678910"
        iban = "12345678"
        val = 1
        ret_val = updateBalance(cpf, iban, val)
        self.assertEqual(ret_val, msg_err_contaNotExists)

    def test_18_updateBalance_03(self):
        print("Test Case 18 - Updating balance adding money with success")
        createNewUser(userTest2["name"], userTest2["surname"], userTest2["cpf"], userTest2["password"])
        cpf = "48775489747"
        conta = getConta(cpf)
        iban = conta["IBAN"]
        val = 2
        ret_val = updateBalance(cpf, iban, val)
        self.assertEqual(ret_val, msg_success)

    def test_19_updateBalance_04(self):
        print("Test Case 19 - Updating balance with a wrong iban format")
        cpf = "48775489747"
        iban = "14587"
        val = 1
        ret_val = updateBalance(cpf, iban, val)
        self.assertEqual(ret_val, msg_err_invalidIban)

    def test_20_updateBalance_03(self):
        print("Test Case 20 - Updating balance with a wrong value")
        cpf = "48775489747"
        conta = getConta(cpf)
        iban = conta["IBAN"]
        val = 0
        ret_val = updateBalance(cpf, iban, val)
        self.assertEqual(ret_val, msg_err_invalidVal)
    


if __name__ == '__main__':
    unittest.main()
