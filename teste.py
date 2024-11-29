from operations.test_operations import (
    makeDeposit,
    makeTransfer,
    loadTransactionsFromFile,
    saveTransactionsToFile,
    getTransactions,
)


def teste():
    # Carrega transações existentes no arquivo
    print("\n### Carregando transações existentes ###")
    loadTransactionsFromFile()
    print("Transações carregadas:", getTransactions())

    # Faz algumas operações
    print("\n### Realizando novas operações ###")
    makeDeposit("12345678900", "IBAN123", 100.0)
    makeTransfer("12345678900", "98765432100", "IBAN123", "IBAN456", 50.0)

    # Exibe a lista de transações após as operações
    print("Transações após operações:", getTransactions())

    # Salva as transações no arquivo (sobrescrevendo o conteúdo)
    print("\n### Salvando transações no arquivo ###")
    saveTransactionsToFile()

    # Carrega novamente para garantir que as duplicatas não aparecem
    print("\n### Carregando transações novamente ###")
    loadTransactionsFromFile()
    print("Transações após carregar novamente:", getTransactions())


if __name__ == "__main__":
    teste()
