import re
from return_messages import *

__all__ = ["createNewUser", "login", "logout", "isLoggedIn", "verifyExistenceUser"]

loggedUserCPF = None
users = []


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
    
    # Regex per verificare che sia una stringa di lunghezza minima 6 caratteri e massima 50
    pattern = r"^.{6,50}$"
    return bool(re.match(pattern, password))


def createNewUser(name, surname, cpf, password):
    from conta import createNewConta

    if is_valid_name_or_surname(name) == False:
        return msg_err_invalidNameSurname
    if is_valid_name_or_surname(surname) == False:
        return msg_err_invalidNameSurname
    
    if len(cpf) != 11 or cpf.isdigit() == False:
        return msg_err_invalidCpf

    if is_valid_password(password) == False:
        return msg_err_invalidPassword

    users.append({"name": name, "surname": surname, "cpf": cpf, "password": password})

    createNewConta(cpf)

    return msg_success


def login(cpf, password):
    if len(cpf) != 11 or cpf.isdigit() == False:
        return msg_err_invalidCpf

    for user in users:
        if user["cpf"] == cpf and user["password"] == password:
            global loggedUserCPF
            loggedUserCPF = cpf
            return msg_success
        
    return msg_err_userNotExists


def logout(cpf):
    if len(cpf) != 11 or cpf.isdigit() == False:
        return msg_err_invalidCpf

    if loggedUserCPF != cpf:
        return msg_err_userNotLoggedIn
    
    loggedUserCPF = None
    return msg_success


def isLoggedIn(cpf):
    if len(cpf) != 11 or cpf.isdigit() == False:
        return msg_err_invalidCpf

    if loggedUserCPF == cpf:
        return True
    else:
        return False
    

def verifyExistenceUser(cpf):
    if len(cpf) != 11 or cpf.isdigit() == False:
        return msg_err_invalidCpf
    
    for user in users:
        if user["cpf"] == cpf :
            return msg_success

    return msg_err_userNotExists
