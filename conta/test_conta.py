import unittest
from conta.conta import *
from conta import contas

# Função para limpar o estado global antes de cada teste
def setup():
    contas.clear()

# Funções de teste
def test_create_new_account():
    setup()  # Limpa a lista de contas antes do teste
    valid_cpf = "12345678900"
    response = createNewConta(valid_cpf)
    assert response['code'] == 0, "Failed to create a new account"

def test_update_balance_success():
    setup()
    valid_cpf = "12345678900"
    createNewConta(valid_cpf)
    valid_iban = contas[0]['IBAN']
    value = 100
    response = updateBalance(valid_cpf, valid_iban, value)
    assert response['code'] == 0, "Failed to update balance"
    assert contas[0]['balance'] == 100, "Balance mismatch after update"

def test_update_balance_invalid_iban():
    setup()
    valid_cpf = "12345678900"
    invalid_iban = "1234567"
    value = 100
    response = updateBalance(valid_cpf, invalid_iban, value)
    assert response['code'] == 4, "Invalid IBAN not detected"

def test_verify_account_existence_success():
    setup()
    valid_cpf = "12345678900"
    createNewConta(valid_cpf)
    valid_iban = contas[0]['IBAN']
    response = verifyExistenceConta(valid_cpf, valid_iban)
    assert response == 0, "Failed to verify account existence"

def test_verify_balance_insufficient_funds():
    setup()
    valid_cpf = "12345678900"
    createNewConta(valid_cpf)
    valid_iban = contas[0]['IBAN']
    value = 1000000
    response = verifyBalance(valid_cpf, valid_iban, value)
    assert response == 6, "Insufficient funds not detected"

# Registrando testes na Test Suite
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.FunctionTestCase(test_create_new_account))
    suite.addTest(unittest.FunctionTestCase(test_update_balance_success))
    suite.addTest(unittest.FunctionTestCase(test_update_balance_invalid_iban))
    suite.addTest(unittest.FunctionTestCase(test_verify_account_existence_success))
    suite.addTest(unittest.FunctionTestCase(test_verify_balance_insufficient_funds))
    return suite

# Executando os testes
if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
