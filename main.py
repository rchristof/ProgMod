import operations
import conta
import user

val = 50
sourceCPF = "12345678901"
destCPF = "12345678902"
sourceIBAN = "12345678"
destIBAN = "12345679" 

print(operations.makeDeposit(sourceCPF, sourceIBAN, val))
print(operations.makeTransfer(sourceCPF, destCPF, sourceIBAN, destIBAN, val+10))
#print(operations.getTransactions())