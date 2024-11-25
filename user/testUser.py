import unittest
from user import *

userTest = {"name": "Mario", "surname": "Rossi", "cpf": "123", "password": "mariorossi1234"}

class TestUser(unittest.TestCase):
    def test_01_createNewUser_ok_ret_val(self):
        print("Test Case 01 - Inserting with success")
        ret_val = createNewUser(userTest["name"], userTest["surname"], userTest["cpf"], userTest["password"],)
        self.assertEqual(ret_val, 0)

    def test_02_createNewUser_ok_created(self):
        print("Test Case 02 - User saved in memory")
        self.assertTrue(verifyExistenceUser)



unittest.main()