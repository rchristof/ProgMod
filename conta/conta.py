from user import *
from return_messages import *
import random

__all__ = ["updateBalance", "verifyExistenceConta", "createNewConta", "verifyBalance", "getConta"]

contas = []

def getConta(CPF):
     """
        Description: Retrieves an account associated with the given CPF.\n
        Coupling:\n
            Input parameters:
                CPF -> the user’s CPF (a string with exactly 11 digits)
            Output values:
                conta -> the account dictionary corresponding to the given CPF, if found
                msg_err_contaNotExists -> if no account exists for the given CPF
        Coupling Conditions:\n
            Entry assertion:
                CPF must be a valid string with exactly 11 numeric digits
            Exit assertion:
                conta -> returned if the account exists for the given CPF
                msg_err_contaNotExists -> returned if no matching account is found
        Restrictions: assumes that the global variable 'contas' is a list of dictionaries where each dictionary represents an account with a 'CPF' field.
    """
    for conta in contas:
        if conta['CPF'] == CPF:
            return conta
    return msg_err_contaNotExists  # Conta not exists

def verifyFormatIban(IBAN):
    """
        Description: Verifies if the IBAN is valid.\n
        Coupling:\n
            Input parameters:
                IBAN -> the IBAN (a string of exactly 8 numeric digits)
            Output values:
                msg_success -> if the IBAN is valid
                msg_err_invalidIban -> if the IBAN is not valid
        Coupling Conditions:\n
            Entry assertion:
                IBAN must be a string
            Exit assertion:
                msg_success -> returned if the IBAN is valid
                msg_err_invalidIban -> returned otherwise
        Restrictions: assumes no additional checks beyond format (length and numeric).
    """
    if isinstance(IBAN, str) and len(IBAN) == 8 and IBAN.isdigit():
        return msg_success  # Success
    return msg_err_invalidIban  # Invalid IBAN format

def createNewConta(CPF):
   """
        Description: Creates a new account for a user associated with the given CPF.\n
        Coupling:\n
            Input parameters:
                CPF -> the user’s CPF (a string with exactly 11 digits)
            Output values:
                msg_success -> if the account was successfully created
                resultVerifyExistenceUser -> if the user does not exist or CPF is invalid
                msg_err_contaAlreadyExists -> if an account for the CPF already exists
        Coupling Conditions:\n
            Entry assertion:
                CPF must correspond to a valid user
            Exit assertion:
                msg_success -> returned if the account was created and stored in 'contas'
                other cases -> no changes to 'contas'
        Restrictions: generates IBAN randomly without checking for collisions.
    """
    resultVerifyExistenceUser = verifyExistenceUser(CPF)
    if resultVerifyExistenceUser != msg_success:
        return resultVerifyExistenceUser  # User not exists or CPF invalid
    
    if verifyExistenceConta(CPF) == msg_success:
        return msg_err_contaAlreadyExists  # Conta already exists

    iban = str(random.randint(10000000, 99999999)) 

    contas.append({"CPF": CPF, "IBAN": iban, "balance": 0})

    return msg_success  # Success

def updateBalance(CPF, IBAN, val):
    """
        Description: Updates the balance of an account identified by CPF and IBAN.\n
        Coupling:\n
            Input parameters:
                CPF -> the user’s CPF (a string with exactly 11 digits)
                IBAN -> the account’s IBAN (a string of exactly 8 numeric digits)
                val -> the value to be added to or deducted from the balance (positive or negative)
            Output values:
                msg_success -> if the balance was updated successfully
                msg_err_invalidVal -> if 'val' is zero or invalid
                msg_err_insufficientBal -> if the deduction exceeds the current balance
                msg_err_contaNotExists -> if no account exists with the given CPF and IBAN
        Coupling Conditions:\n
            Entry assertion:
                CPF and IBAN must be valid, and 'val' must be non-zero
            Exit assertion:
                msg_success -> balance updated if conditions are met
                other cases -> no changes to the balance
        Restrictions: assumes no concurrent access to 'contas'.
    """
    format_check = verifyFormatIban(IBAN)
    if format_check["code"] != 0:
        return format_check  # Return error message from verifyFormatIban

    if not isinstance(val, (int, float)) or val == 0:
        return msg_err_invalidVal  # Invalid val

    for conta in contas:
        if conta['CPF'] == CPF and conta['IBAN'] == IBAN:
            if conta['balance'] + val < 0:
                return msg_err_insufficientBal  # Insufficient balance
            conta['balance'] += val
            return msg_success  # Success

    return msg_err_contaNotExists  # Conta not exists

def verifyExistenceConta(CPF, IBAN=None):
    """
        Description: Verifies the existence of an account associated with the given CPF and optionally a specific IBAN.\n
        Coupling:\n
            Input parameters:
                CPF -> the user’s CPF (a string with exactly 11 digits)
                IBAN -> optional, the account’s IBAN (a string of exactly 8 numeric digits)
            Output values:
                msg_success -> if the account exists
                msg_err_contaNotExists -> if the account does not exist
        Coupling Conditions:\n
            Entry assertion:
                CPF must be valid
            Exit assertion:
                msg_success -> if a matching account is found
                msg_err_contaNotExists -> otherwise
        Restrictions: assumes global 'contas' has unique CPF-IBAN combinations.
    """
    if len(CPF) != 11 or CPF.isdigit() == False:
            return msg_err_invalidCpf

    for conta in contas:
        if conta['CPF'] == CPF:
            if IBAN is None or conta['IBAN'] == IBAN:
                return msg_success  # Success
    return msg_err_contaNotExists  # Conta not exists

def verifyBalance(CPF, IBAN, val):
    """
        Description: Verifies if the account has sufficient balance for a given value.\n
        Coupling:\n
            Input parameters:
                CPF -> the user’s CPF (a string with exactly 11 digits)
                IBAN -> the account’s IBAN (a string of exactly 8 numeric digits)
                val -> the amount to be checked (a positive number)
            Output values:
                msg_success -> if the account has sufficient balance
                msg_err_invalidVal -> if 'val' is invalid
                msg_err_insufficientBal -> if the account’s balance is less than 'val'
                msg_err_contaNotExists -> if no account exists with the given CPF and IBAN
        Coupling Conditions:\n
            Entry assertion:
                CPF and IBAN must be valid, and 'val' must be positive
            Exit assertion:
                msg_success -> if sufficient balance exists
                other cases -> no changes to the account
        Restrictions: assumes no concurrent balance modifications.
    """
    if not isinstance(val, (int, float)) or val <= 0:
        return msg_err_invalidVal  # Invalid val

    # Encontra a conta correspondente
    for conta in contas:
        if conta['CPF'] == CPF and conta['IBAN'] == IBAN:
            if conta['balance'] >= val:
                return msg_success  # Success
            return msg_err_insufficientBal  # Insufficient balance

    return msg_err_contaNotExists   # Conta not exists
