import re
from return_messages import *
import json
import os

__all__ = ["createNewUser", "login", "logout", "isLoggedIn", "verifyExistenceUser", "getAccountInfo", "loadUsersFromFile", "saveUsersToFile"]

loggedUserCPF = None
_users = []


def getUsers():
    """
    Description: Retrieves a copy of the current users list.\n
    Coupling:\n
        Input parameters: none
        Output values:
            - A list of user dictionaries currently stored in memory.
    Coupling Conditions:\n
        Entry assertion: none
        Exit assertion:
            - A copy of the users list is returned without modifying the original list.
    Restrictions: The returned list is independent of the original and modifications to it do not affect the global `_users`.
    """

    return _users.copy()


def setUsers(transactions):
    """
    Description: Replaces the current users list with a new one.\n
    Coupling:\n
        Input parameters:
            - transactions -> A list of user dictionaries to replace the current list.
        Output values: none
    Coupling Conditions:\n
        Entry assertion:
            - The input must be a valid list of dictionaries formatted as users.
        Exit assertion:
            - The global `_users` list is replaced with the provided one.
    Restrictions: Assumes the provided list contains valid user dictionaries and does not validate its content.
    """

    _users.clear()
    _users.extend(transactions)


def loadUsersFromFile():
    """
    Description: Loads users from a file into memory.\n
    Coupling:\n
        Input parameters: none
        Output values: none
    Coupling Conditions:\n
        Entry assertion:
            - The file should exist at the predefined path and be formatted as a valid JSON list of users.
        Exit assertion:
            - The global `_users` list is updated with the content of the file.
            - If the file is missing or invalid, `_users` is set to an empty list.
    Restrictions:
        - If the file is malformed (not a valid JSON), `_users` is cleared.
        - Assumes the file path is correctly defined as `database/users/_users.txt`.
    """

    file_path="database/users/_users.txt"
    try:
        with open(file_path, "r") as file:
            transactions = json.load(file)
            setUsers(transactions)  # Atualiza a lista de transações
    except FileNotFoundError:
        setUsers([])  # Inicializa a lista como vazia
    except json.JSONDecodeError:
        setUsers([])


def saveUsersToFile():
    """
    Description: Saves the current users list to a file.\n
    Coupling:\n
        Input parameters: none
        Output values: none
    Coupling Conditions:\n
        Entry assertion:
            - The global `_users` list must be a valid list of user dictionaries.
        Exit assertion:
            - The contents of `_users` are written to the predefined file path in JSON format.
    Restrictions:
        - The file path is predefined as `database/users/_users.txt`.
        - Assumes the directory structure exists and is writable.
    """

    file_path="database/users/_users.txt"
    with open(file_path, "w") as file:
        json.dump(getUsers(), file, indent=4)  # Obtém a lista atual

def getAccountInfo(cpf):
    if len(cpf) != 11 or cpf.isdigit() == False:
        return msg_err_invalidCpf

    # Verifica se o usuário está logado
    resultIsLoggedIn = isLoggedIn(cpf)
    if resultIsLoggedIn != msg_success:
        return resultIsLoggedIn

    for user in _users:
        if user["cpf"] == cpf:
            from conta import getConta
            resultGetConta = getConta(cpf)
            if resultGetConta == msg_err_contaNotExists:
                return resultGetConta

            return {"Name": user["name"], "Surname": user["surname"], "CPF": user["cpf"], "IBAN": resultGetConta["IBAN"], "Password": user["password"], "Balance": resultGetConta["balance"]}
    return msg_err_userNotExists


def createNewUser(name, surname, cpf, password):
    """
        Description: implements Account Creation requirements\n
        Coupling:\n
            Input parameters:
                name -> user’s first name (a not empty string with at most 50 chars, which can only contain alphabetic chars, spaces, "'" and "-")
                surname -> user’s last name (same format of name)
                cpf -> user’s CPF (a string with exactly 11 digits)
                password -> user’s password (a string with at least 4 chars and at most 50 chars)
            Output values:
                msg_err_invalidNameSurname -> if name and/or surname are not valid
                msg_err_invalidCpf -> if CPF is not valid
                msg_err_invalidPassword -> if CPF is not valid
                msg_err_userAlreadyExists -> if a user with the given CPF already exists
                msg_err_contaAlreadyExists -> if a conta with the given CPF already exists
                msg_success -> if the user and the conta are created correctly
        Coupling Conditions:\n
            entry assertion: none
            exit assertion:
                msg_success -> the user and the conta are saved in memory
                msg_err_contaAlreadyExists -> just the user is saved in memory
                other cases -> none
    """
    from conta import createNewConta

    # Regex per verificare che sia una stringa non vuota che può contenere solo caratteri alfabetici, spazi, apostrofi
    # e trattini, di lunghezza massima 50 caratteri
    pattern = r"^[a-zA-Z'’ -]{1,50}$"
    isValidNameOrSurn = isinstance(name, str) and isinstance(surname, str) and (bool(re.match(pattern, name)) and bool(re.match(pattern, surname)))
    if not isValidNameOrSurn:
        print("\nError: " + msg_err_invalidNameSurname["message"])
        return msg_err_invalidNameSurname
    
    if len(cpf) != 11 or cpf.isdigit() == False:
        print("\nError: " + msg_err_invalidCpf["message"])
        return msg_err_invalidCpf

    # Regex per verificare che sia una stringa di lunghezza minima 4 caratteri e massima 50
    pattern = r"^.{4,50}$"
    isValidPassword = isinstance(password, str) and bool(re.match(pattern, password))
    if not isValidPassword:
        print("\nError: " + msg_err_invalidPassword["message"])
        return msg_err_invalidPassword
    
    for user in _users:
        if user["cpf"] == cpf:
            print("\nError: " + msg_err_userAlreadyExists["message"])
            return msg_err_userAlreadyExists

    _users.append({"name": name, "surname": surname, "cpf": cpf, "password": password})

    resultCreateNewConta = createNewConta(cpf)
    if resultCreateNewConta != msg_success:
        print("\nError: " + resultCreateNewConta["message"])
        return resultCreateNewConta

    print("\nSuccessful user and conta creation")
    return msg_success


def login(cpf, password):
    """
        Description: implements Login requirement\n
        Coupling:\n
            Input parameters:
                cpf -> user’s CPF (a string with exactly 11 digits)
                password -> user’s password (a string with at least 4 chars and at most 50 chars)
            Output values:
                msg_err_invalidCpf -> if CPF is not valid
                msg_err_userNotExists -> if a user with the given CPF and password doesn’t exist
                msg_success -> if the user has been logged in with success
        Coupling Conditions:\n
            entry assertion: none
            exit assertion:
                msg_success -> user’s CPF is saved in memory as the current logged one, eventually overriding the previous one
                other cases -> none
        Restrictions: the cases of a) password not valid, b) cpf existing but wrong password and c) cpf not existing are all grouped in the same error message output value,
        so the function caller can't know which one triggered the error
    """
    if len(cpf) != 11 or cpf.isdigit() == False:
        print("\nError: " + msg_err_invalidCpf["message"])
        return msg_err_invalidCpf

    for user in _users:
        if user["cpf"] == cpf and user["password"] == password:
            global loggedUserCPF
            loggedUserCPF = cpf
            print("\nSuccessful login")
            return msg_success
        
    print("\nError: " + msg_err_userNotExists["message"] + " (wrong CPF and/or password) ")
    return msg_err_userNotExists


def logout(cpf):
    if len(cpf) != 11 or cpf.isdigit() == False:
        print("\nError: " + msg_err_invalidCpf["message"])
        return msg_err_invalidCpf

    global loggedUserCPF
    if loggedUserCPF != cpf:
        print("\nError: " + msg_err_userNotLoggedIn["message"])
        return msg_err_userNotLoggedIn
    
    loggedUserCPF = None
    print("\nSuccessful logout")
    return msg_success


def isLoggedIn(cpf):
    if len(cpf) != 11 or cpf.isdigit() == False:
        return msg_err_invalidCpf

    if loggedUserCPF == cpf:
        return msg_success
    else:
        return msg_err_userNotLoggedIn
    

def verifyExistenceUser(cpf):
    if len(cpf) != 11 or cpf.isdigit() == False:
        return msg_err_invalidCpf
    
    for user in _users:
        if user["cpf"] == cpf :
            return msg_success

    return msg_err_userNotExists
