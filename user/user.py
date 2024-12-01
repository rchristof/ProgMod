import re
from return_messages import *

__all__ = ["createNewUser", "login", "logout", "isLoggedIn", "verifyExistenceUser", "getAccountInfo"]

loggedUserCPF = None
users = []


def getAccountInfo(cpf):
    if len(cpf) != 11 or cpf.isdigit() == False:
        return msg_err_invalidCpf

    # Verifica se o usuário está logado
    resultIsLoggedIn = isLoggedIn(cpf)
    if resultIsLoggedIn != msg_success:
        return resultIsLoggedIn

    for user in users:
        if user["cpf"] == cpf:
            from conta import getConta
            resultGetConta = getConta(cpf)
            if resultGetConta == msg_err_contaNotExists:
                return resultGetConta

            return {"Name": user["name"], "Surname": user["surname"], "CPF": user["cpf"], "IBAN": resultGetConta["IBAN"], "Balance": resultGetConta["balance"]}
    return msg_err_userNotExists

def is_valid_name_or_surname(name):
    if not isinstance(name, str):
        return False
    
    # Regex per verificare che sia una stringa non vuota che può contenere solo caratteri alfabetici, spazi, apostrofi
    # e trattini, di lunghezza massima 50 caratteri
    pattern = r"^[a-zA-Z'’ -]{1,50}$"
    return bool(re.match(pattern, name))

def is_valid_password(password):
    if not isinstance(password, str):
        return False
    
    # Regex per verificare che sia una stringa di lunghezza minima 4 caratteri e massima 50
    pattern = r"^.{4,50}$"
    return bool(re.match(pattern, password))


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

    if is_valid_name_or_surname(name) == False or is_valid_name_or_surname(surname) == False:
        print("Error: " + msg_err_invalidNameSurname["message"])
        return msg_err_invalidNameSurname
    
    if len(cpf) != 11 or cpf.isdigit() == False:
        print("Error: " + msg_err_invalidCpf["message"])
        return msg_err_invalidCpf

    if is_valid_password(password) == False:
        print("Error: " + msg_err_invalidPassword["message"])
        return msg_err_invalidPassword
    
    for user in users:
        if user["cpf"] == cpf:
            print("Error: " + msg_err_userAlreadyExists["message"])
            return msg_err_userAlreadyExists

    users.append({"name": name, "surname": surname, "cpf": cpf, "password": password})

    resultCreateNewConta = createNewConta(cpf)
    if resultCreateNewConta != msg_success:
        print("Error: " + resultCreateNewConta["message"])
        return resultCreateNewConta

    print("Successful user and conta creation")
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
        print("Error: " + msg_err_invalidCpf["message"])
        return msg_err_invalidCpf

    for user in users:
        if user["cpf"] == cpf and user["password"] == password:
            global loggedUserCPF
            loggedUserCPF = cpf
            print("Successful login")
            return msg_success
        
    print("Error: " + msg_err_userNotExists["message"])
    return msg_err_userNotExists


def logout(cpf):
    if len(cpf) != 11 or cpf.isdigit() == False:
        print("Error: " + msg_err_invalidCpf["message"])
        return msg_err_invalidCpf

    global loggedUserCPF
    if loggedUserCPF != cpf:
        print("Error: " + msg_err_userNotLoggedIn["message"])
        return msg_err_userNotLoggedIn
    
    loggedUserCPF = None
    print("Successful logout")
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
    
    for user in users:
        if user["cpf"] == cpf :
            return msg_success

    return msg_err_userNotExists
