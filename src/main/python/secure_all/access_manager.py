"""Module AccessManager with AccessManager Class """

from secure_all.data.access_key import AccessKey
from secure_all.data.access_request import AccessRequest
from secure_all.data.access_revoqued import TypeAccessRevoqued, RevoqueStore


class AccessManager:
    """AccessManager class, manages the access to a building implementing singleton """

    # pylint: disable=too-many-arguments,no-self-use,invalid-name, too-few-public-methods
    class __AccessManager:
        """Class for providing the methods for managing the access to a building"""

        @staticmethod
        def request_access_code(id_card, name_surname, access_type, email_address, days):
            """ this method give access to the building"""
            my_request = AccessRequest(id_card, name_surname, access_type, email_address, days)
            my_request.store_request()
            return my_request.access_code

        @staticmethod
        def get_access_key(keyfile):
            """Returns the access key for the access code & dni received in a json file"""
            my_key = AccessKey.create_key_from_file(keyfile)
            my_key.store_keys()
            return my_key.key

        @staticmethod
        def revoke_key(file_path):
            """This method cancel a key"""
            key_revoque = TypeAccessRevoqued.create_key_from_file(file_path)
            key_revoque.check_validity()
            key_revoque.store_revoque()
            return key_revoque.emails()

        @staticmethod
        def open_door(key):
            """Opens the door if the key is valid an it is not expired"""
            my_key = AccessKey.create_key_from_id(key)
            if my_key:
                request = RevoqueStore()
                request.search_revoque(key)
                my_key.store_access()
            return AccessKey.create_key_from_id(key).is_valid()

    __instance = None

    def __new__(cls):
        if not AccessManager.__instance:
            AccessManager.__instance = AccessManager.__AccessManager()
        return AccessManager.__instance
