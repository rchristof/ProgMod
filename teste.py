import operations.test_operations as operations

def teste():
    operations.makeDeposit("12345678900", "IBAN123", 100.0)
    operations.makeTransfer("12345678900", "98765432100", "IBAN123", "IBAN456", 50.0)
    operations.generateReport("12345678900", "IBAN123")

if __name__ == "__main__":
    teste()
