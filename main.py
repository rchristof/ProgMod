import sys  # Per chiudere l'applicazione in modo pulito
import user
import conta
import operations
import return_messages

def main_menu():
    user.loadUsersFromFile()
    conta.loadContasFromFile()
    operations.loadTransactionsFromFile()
    while True:
        # Principal menu
        print("\n\n===== Main Menu =====")
        print("1. Create a new user")
        print("2. Login")
        print("3. Exit")

        try:
            
            choice = int(input("\nEnter your choice (1-3): "))

            if choice == 1:
                user_create_user()

            elif choice == 2:
                result = user_login()
                if result != None:
                    cpf = result
                    menu_logged_user(cpf)

            elif choice == 3:
                print("\nExiting the application. Goodbye!\n")
                conta.saveContasToFile()
                user.saveUsersToFile()
                operations.saveTransactionsToFile()
                sys.exit(0)  

            else:
                print("\nInvalid choice. Please enter a number between 1 and 3.")

        except ValueError:
            print("\nInvalid input. Please enter a valid number.")

def menu_logged_user(cpf):
    name = user.getAccountInfo(cpf)["Name"]
    print(f"\n\nWelcome {name}!")

    while True:
        print("\n===== Logged User Menu =====")
        print("1. Get info account (IBAN, balance and personal data)")
        print("2. Money deposit")
        print("3. Money transfer")
        print("4. Transactions report generation")
        print("5. Logout")

        try:
            choice = int(input("\nEnter your choice (1-5): "))

            if choice == 1:
                user_get_info_account(cpf)
            elif choice == 2:
                user_money_deposit(cpf)
            elif choice == 3:
                user_money_transfer(cpf)
            elif choice == 4:
                operations.generateReport(cpf, user.getAccountInfo(cpf)["IBAN"])
            elif choice == 5:
                user.logout(cpf)
                break
            else:
                print("\nInvalid choice. Please enter a number between 1 and 5.")
        except ValueError:
            print("\nInvalid input. Please enter a valid number.")

def user_money_transfer(cpf):
    print("\n--- Money Transfer ---")
    dest_cpf = input("Insert the destination CPF (11 digits): ")
    dest_iban = input("Insert the destination IBAN (8 digits): ")
    value = float(input("Insert the value to transfer: "))
    operations.makeTransfer(cpf, dest_cpf, user.getAccountInfo(cpf)["IBAN"], dest_iban, value)

def user_money_deposit(cpf):
    print("\n--- Money Deposit ---")
    value = float(input("Insert the value to deposit: "))
    operations.makeDeposit(cpf, user.getAccountInfo(cpf)["IBAN"], value)

def user_get_info_account(cpf):
    account = user.getAccountInfo(cpf)
    print("\n--- Account Info ---")
    print(f"Name: {account['Name']}")
    print(f"Surname: {account['Surname']}")
    print(f"CPF: {account['CPF']}")
    print(f"IBAN: {account['IBAN']}")
    print(f"Password: {account['Password']}")
    print(f"Balance: {account['Balance']} reais")
    print("--------------------")

def user_create_user():

    print("\n--- Create a new User ---")

    name = input("Insert your name: ")
    surname = input("Insert your surname: ")
    cpf = input("Insert your CPF (11 digits): ")
    password = input("Insert your password (at least 4 char): ")

    result = user.createNewUser(name, surname, cpf, password)
    if(result != return_messages.msg_success):
        print("Account not created")

def user_login():
    print("\n--- Login ---")
    cpf = input("Insert your CPF (11 digits): ")
    password = input("Insert your password (at least 4 char): ")

    result = user.login(cpf, password)
    if(result != return_messages.msg_success):
        print("Login failed")
        return None
    else:
        return cpf

if __name__ == "__main__":
    main_menu()