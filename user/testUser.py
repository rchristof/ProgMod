import unittest
from user import *
from conta import getConta
from return_messages import *

userTest = {"name": "Mario", "surname": "Rossi", "cpf": "12345678910", "password": "mariorossi1234"}
userTest2 = {"name": "Gianni", "surname": "Verdi", "cpf": "22345678910", "password": "giannigianni"}


class TestUser(unittest.TestCase):
    def test_01_createNewUser_ok_ret_val(self):
        print("Test Case 01 - Inserting user with success")
        ret_val = createNewUser(userTest["name"], userTest["surname"], userTest["cpf"], userTest["password"])
        self.assertEqual(ret_val, msg_success)

    def test_02_createNewUser_ok_created(self):
        print("Test Case 02 - User saved in memory")
        self.assertTrue(verifyExistenceUser)

    def test_03_createNewUser_nok_invalid_name(self):
        print("Test Case 03 - Not inserting, name invalid")
        ret_val = createNewUser("Abc123", userTest["surname"], userTest["cpf"], userTest["password"])
        self.assertEqual(ret_val, msg_err_invalidNameSurname)

    def test_04_createNewUser_nok_invalid_surname(self):
        print("Test Case 04 - Not inserting, surname invalid")
        ret_val = createNewUser(userTest["name"], "Abc123", userTest["cpf"], userTest["password"])
        self.assertEqual(ret_val, msg_err_invalidNameSurname)

    def test_05_createNewUser_nok_invalid_cpf(self):
        print("Test Case 05 - Not inserting, CPF invalid")
        ret_val = createNewUser(userTest["name"], userTest["surname"], "123", userTest["password"])
        self.assertEqual(ret_val, msg_err_invalidCpf)

    def test_06_createNewUser_nok_invalid_password(self):
        print("Test Case 06 - Not inserting, CPF invalid")
        ret_val = createNewUser(userTest["name"], userTest["surname"], userTest["cpf"], "12")
        self.assertEqual(ret_val, msg_err_invalidPassword)

    def test_07_createNewUser_nok_invalid_password(self):
        print("Test Case 07 - Not inserting, user already existing")
        ret_val = createNewUser(userTest["name"], userTest["surname"], userTest["cpf"], userTest["password"])
        self.assertEqual(ret_val, msg_err_userAlreadyExists)


    def test_08_login_ok_ret_val(self):
        print("Test Case 08 - Login with success")
        ret_val = login(userTest["cpf"], userTest["password"])
        self.assertEqual(ret_val, msg_success)

    def test_09_login_ok_logged(self):
        print("Test Case 09 - User actually logged")
        ret_val = isLoggedIn(userTest["cpf"])
        self.assertEqual(ret_val, msg_success)

    def test_10_login_ok_w_other_user(self):
        print("Test Case 10 - Login with another user")
        # creating a new user
        ret_val = createNewUser(userTest2["name"], userTest2["surname"], userTest2["cpf"], userTest2["password"])
        self.assertEqual(ret_val, msg_success)
        # login with this new user
        ret_val = login(userTest2["cpf"], userTest2["password"])
        self.assertEqual(ret_val, msg_success)
        ret_val = isLoggedIn(userTest2["cpf"])
        self.assertEqual(ret_val, msg_success)
        # old user not logged in anymore
        ret_val = isLoggedIn(userTest["cpf"])
        self.assertEqual(ret_val, msg_err_userNotLoggedIn)

    def test_11_login_nok_invalid_cpf(self):
        print("Test Case 11 - Login with invalid CPF")
        ret_val = login("1234", userTest["password"])
        self.assertEqual(ret_val, msg_err_invalidCpf)

    def test_12_login_nok_user_not_exists(self):
        print("Test Case 12 - Login with a non existing user")
        ret_val = login("02345678910", "123")
        self.assertEqual(ret_val, msg_err_userNotExists)

    def test_13_login_nok_wrong_password(self):
        print("Test Case 13 - Login with correct CPF but wrong password")
        ret_val = login(userTest["cpf"], "123")
        self.assertEqual(ret_val, msg_err_userNotExists)


    def test_14_logout_ok_ret_val(self):
        print("Test Case 14 - Logout with success")
        ret_val = logout(userTest2["cpf"])
        self.assertEqual(ret_val, msg_success)

    def test_15_logout_ok_logged_out(self):
        print("Test Case 15 - User actually logged out")
        ret_val = isLoggedIn(userTest2["cpf"])
        self.assertEqual(ret_val, msg_err_userNotLoggedIn)

    def test_16_logout_nok_invalid_cpf(self):
        print("Test Case 16 - Logout with invalid cpf")
        ret_val = logout("1234")
        self.assertEqual(ret_val, msg_err_invalidCpf)
        
    def test_17_logout_nok_user_not_logged(self):
        print("Test Case 17 - Logout of a not logged user")
        # login of userTest
        login(userTest["cpf"], userTest["password"])
        ret_val = logout(userTest2["cpf"])
        self.assertEqual(ret_val, msg_err_userNotLoggedIn)

    def test_18_logout_nok_user_not_existing(self):
        print("Test Case 18 - Logout of a not existing user")
        ret_val = logout("02345678910")
        self.assertEqual(ret_val, msg_err_userNotLoggedIn)


    def test_19_isLoggedIn_ok(self):
        print("Test Case 11 - isLoggedIn, user is logged in")
        ret_val = isLoggedIn(userTest["cpf"])
        self.assertEqual(ret_val, msg_success)

    def test_20_isLoggedIn_nok_invalid_cpf(self):
        print("Test Case 20 - isLoggedIn, CPF invalid")
        ret_val = isLoggedIn("1234")
        self.assertEqual(ret_val, msg_err_invalidCpf)

    def test_21_isLoggedIn_nok_user_not_logged(self):
        print("Test Case 21 - isLoggedIn, user not logged in")
        ret_val = isLoggedIn(userTest2["cpf"])
        self.assertEqual(ret_val, msg_err_userNotLoggedIn)

    def test_22_isLoggedIn_nok_user_not_existing(self):
        print("Test Case 22 - isLoggedIn, user not exisiting")
        ret_val = isLoggedIn("02345678910")
        self.assertEqual(ret_val, msg_err_userNotLoggedIn)

    
    def test_23_verifyExistenceUser_ok(self):
        print("Test Case 23 - verifyExistenceUser, users existing")
        ret_val = verifyExistenceUser(userTest["cpf"])
        self.assertEqual(ret_val, msg_success)
        ret_val = verifyExistenceUser(userTest2["cpf"])
        self.assertEqual(ret_val, msg_success)

    def test_24_verifyExistenceUser_nok_invalid_cpf(self):
        print("Test Case 24 - verifyExistenceUser, CPF invalid")
        ret_val = verifyExistenceUser("1234")
        self.assertEqual(ret_val, msg_err_invalidCpf)

    def test_25_verifyExistenceUser_nok_user_not_existing(self):
        print("Test Case 25 - verifyExistenceUser, user not existing")
        ret_val = verifyExistenceUser("02345678910")
        self.assertEqual(ret_val, msg_err_userNotExists)


    def test_26_getAccountInfo_ok(self):
        print("Test Case 26 - getAccountInfo, user existing")
        ret_val = getAccountInfo(userTest["cpf"])
        resultGetConta = getConta(userTest["cpf"])
        self.assertEqual(
            ret_val,
            {"Name": userTest["name"], "Surname": userTest["surname"], "CPF": userTest["cpf"], "IBAN": resultGetConta["IBAN"], "Balance": resultGetConta["balance"]}
        )

    def test_27_getAccountInfo_nok_invalid_cpf(self):
        print("Test Case 27 - getAccountInfo, CPF invalid")
        ret_val = getAccountInfo("1234")
        self.assertEqual(ret_val, msg_err_invalidCpf)

    def test_28_getAccountInfo_nok_user_not_existing(self):
        print("Test Case 28 - getAccountInfo, user not existing")
        ret_val = getAccountInfo("02345678910")
        self.assertEqual(ret_val, msg_err_userNotLoggedIn)

    def test_29_getAccountInfo_nok_user_not_logged(self):
        print("Test Case 29 - getAccountInfo, user not logged in")
        ret_val = getAccountInfo(userTest2["cpf"])
        self.assertEqual(ret_val, msg_err_userNotLoggedIn)

unittest.main()