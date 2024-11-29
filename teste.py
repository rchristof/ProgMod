from operations import makeDeposit, makeTransfer, generateReport

def teste():
    makeDeposit("12345678900", "IBAN123", 100.0)
    makeTransfer("12345678900", "98765432100", "IBAN123", "IBAN456", 50.0)
    generateReport("12345678900", "IBAN123")

if __name__ == "__main__":
    teste()
