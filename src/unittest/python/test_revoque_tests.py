"""Test module for testing get_access_key"""
import unittest
import csv

from secure_all import AccessManager, AccessManagementException, \
    JSON_FILES_PATH, KeysJsonStore, RequestJsonStore, RevoqueStore


class TestRevoque(unittest.TestCase):
    """Test class for testing get_access_key"""

    # pylint: disable=no-member
    @classmethod
    def setUpClass(cls) -> None:
        """Removing the Stores and creating required AccessRequest for testing"""
        # pylint: disable=no-member

        requests_store = RequestJsonStore()
        requests_store.empty_store()
        keys_store = KeysJsonStore()
        keys_store.empty_store()
        revoque = RevoqueStore()
        revoque.empty_store()

        # introduce a key valid and not expired and guest
        my_manager = AccessManager()
        print("one")
        my_manager.request_access_code("05270358T", "Pedro Martin",
                                       "Resident", "uc3m@gmail.com", 0)
        print("two")
        my_manager.request_access_code("87654123L", "Maria Montero",
                                       "Guest", "maria@uc3m.es", 15)

        print("three")
        my_manager.request_access_code("53935158C", "Marta Lopez",
                                       "Guest", "uc3m@gmail.com", 5)
        file_name = JSON_FILES_PATH + "key_ok.json"
        my_manager.get_access_key(file_name)
        file_name = JSON_FILES_PATH + "key_ok2.json"
        my_manager.get_access_key(file_name)
        file_name = JSON_FILES_PATH + "key_ok3_resident.json"
        my_manager.get_access_key(file_name)
        file_name = JSON_FILES_PATH + "key_alredy_revoqued.json"
        my_manager.revoke_key(file_name)
        print("Finished init")

    def test_clase_valida(self):
        """Clase para testear el return de un revoque valido"""
        my_code = AccessManager()
        my_cases = JSON_FILES_PATH + "revoke_valido.json"
        valor = my_code.revoke_key(my_cases)
        self.assertEqual(['mail1@uc3m.es', 'mail2@uc3m.es'], valor)

    def test_parametrized_cases_tests(self):
        """Parametrized cases read from testingCases_RF1.csv"""
        my_cases = JSON_FILES_PATH + "testingCases_RF3.csv"
        with open(my_cases, newline='', encoding='utf-8') as csvfile:
            # pylint: disable=no-member
            param_test_cases = csv.DictReader(csvfile, delimiter=';')
            my_code = AccessManager()
            for row in param_test_cases:
                file_name = JSON_FILES_PATH + row["FILE"]
                print("Param:" + row['ID TEST'] + row["VALID INVALID"])
                if row["VALID INVALID"] == "VALID":
                    valor = my_code.RevokeKey(file_name)
                    self.assertEqual(row["EXPECTED RESULT"], valor)
                    print("el valor: " + valor)
                else:
                    with self.assertRaises(AccessManagementException) as c_m:
                        my_code.revoke_key(file_name)
                    self.assertEqual(c_m.exception.message, row["EXPECTED RESULT"])


if __name__ == '__main__':
    unittest.main()
