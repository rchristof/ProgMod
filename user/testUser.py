import unittest
from user import *

msg_success = {"code": 0, "message": "Success"}
msg_err_invalidNameSurname = {"code": 9, "message": "Invalid name/surname"}
msg_err_invalidCpf = {"code": 8, "message": "Invalid cpf"}
msg_err_invalidPassword = {"code": 7, "message": "Invalid password"}
msg_err_userNotExists = {"code": 3, "message": "User not exists"}
msg_err_userNotLoggedIn = {"code": 1, "message": "User not logged in"}

userTest = {"name": "Mario", "surname": "Rossi", "cpf": "123", "password": "mariorossi1234"}

class TestUser(unittest.TestCase):
    def test_01_createNewUser_ok_ret_val(self):
        print("Test Case 01 - Inserting with success")
        ret_val = user.createNewUser(userTest["name"], userTest["surname"], userTest["cpf"], userTest["password"])
        self.assertEqual(ret_val, 0)

    def test_02_createNewUser_ok_created(self):
        print("Test Case 02 - User saved in memory")
        self.assertTrue(verifyExistenceUser)

    def test03_createNewUser_nok_invalid_name(self):
        print("Test Case 03 - Not inserting, name invalid")
        ret_val = createNewUser("Abc123", userTest["surname"], userTest["cpf"], userTest["password"])
        self.assertEqual(ret_val, msg_err_invalidNameSurname)



unittest.main()