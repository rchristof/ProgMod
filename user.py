import re

__all__ = ["createNewUser","login", "logout","isLoggedIn", "verifyExistenceUser"]

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
    if is_valid_name_or_surname(name) == False:
        return 9    # Invalid name/surname code
    if is_valid_name_or_surname(surname) == False:
        return 9    # Invalid name/surname code
    
    # validazione CPF: come gestiamo la funzione di validazione del cpf a livello di moduli?

    if is_valid_password(password) == False:
        return 7    # Invalid password code


    #chiamata createNewConta(cpf) e gestione varie casistiche sui parametri di ritorno
    

    users.append({"name": name, "surname": surname, "cpf": cpf, "password": password})
    return 0    # Success code


def login(cpf, password):
    # validazione CPF: come gestiamo la funzione di validazione del cpf a livello di moduli?

    for user in users:
        if user["cpf"] == cpf and user["password"] == password:
            global loggedUserCPF
            loggedUserCPF = cpf
            return 0    # Success code

    return 3    # User not exists code


def logout(cpf):
    # validazione CPF: come gestiamo la funzione di validazione del cpf a livello di moduli?

    if loggedUserCPF != cpf:
        return 1    # User not logged in code
    
    loggedUserCPF = None
    return 0    # Success code


def isLoggedIn(cpf):
    # validazione CPF: come gestiamo la funzione di validazione del cpf a livello di moduli?

    if loggedUserCPF == cpf:
        return True
    else:
        return False
    

def verifyExistenceUser(cpf):
    # validazione CPF: come gestiamo la funzione di validazione del cpf a livello di moduli?
    
    for user in users:
        if user["cpf"] == cpf :
            return True

    return False
