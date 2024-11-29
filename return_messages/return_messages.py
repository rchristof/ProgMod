__all__ = [
        "msg_success",
        "msg_err_userNotLoggedIn",
        "msg_err_contaNotExists",
        "msg_err_userNotExists",
        "msg_err_invalidIban",
        "msg_err_invalidVal",
        "msg_err_insufficientBal",
        "msg_err_invalidPassword",
        "msg_err_invalidCpf",
        "msg_err_invalidNameSurname"
    ]

msg_success = {"code": 0, "message": "Success"}
msg_err_userNotLoggedIn = {"code": 1, "message": "User not logged in"}
msg_err_contaNotExists = {"code": 2, "message": "Conta not exists"}
msg_err_userNotExists = {"code": 3, "message": "User not exists"}
msg_err_invalidIban = {"code": 4, "message": "Invalid IBAN"}
msg_err_invalidVal = {"code": 5, "message": "Invalid val"}
msg_err_insufficientBal = {"code": 6, "message": "Insufficient balance"}
msg_err_invalidPassword = {"code": 7, "message": "Invalid password"}
msg_err_invalidCpf = {"code": 8, "message": "Invalid cpf"}
msg_err_invalidNameSurname = {"code": 9, "message": "Invalid name/surname"}