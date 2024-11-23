from operations import Operations

def main():
    # Inicializa o módulo Operations
    operations = Operations()

    # Teste de Depósito
    print("=== Teste de Depósito ===")
    result_deposit = operations.makeDeposit("12345678900", "IBAN123", 100.0)
    print("Resultado:", result_deposit)
    print("Transações:", operations.transactions)

    # Teste de Transferência
    print("\n=== Teste de Transferência ===")
    result_transfer = operations.makeTransfer("12345678900", "98765432100", "IBAN123", "IBAN456", 50.0)
    print("Resultado:", result_transfer)
    print("Transações:", operations.transactions)

    # Teste de Geração de Relatório (IBAN com depósito e transferência)
    print("\n=== Teste de Geração de Relatório ===")
    result_report = operations.generateReport("12345678900", "IBAN123")
    print("Resultado:", result_report)

    # Teste de Geração de Relatório (IBAN sem transações)
    print("\n=== Teste de Geração de Relatório para IBAN sem transações ===")
    result_empty_report = operations.generateReport("12345678900", "IBAN789")
    print("Resultado:", result_empty_report)

if __name__ == "__main__":
    main()
