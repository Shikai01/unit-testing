"""Objeto access_revoque que se usara para remover una key"""
import json
from datetime import datetime
from secure_all.data.attributes.attribute_key import Key
from secure_all.exception.access_management_exception import AccessManagementException
from secure_all.data.attributes.atrribute_reason import ReasonAtributte
from secure_all.data.attributes.attribute_revoque import RevoqueAtributte
from secure_all.storage.keys_json_store import KeysJsonStore
from secure_all.storage.revoque_json import RevoqueStore
from secure_all.parser.desactivar_json_parser import DesactivarJson


class TypeAccessRevoqued:
    """Class representing the access request"""

    # pylint: disable=too-many-arguments

    def __init__(self, key, revocation, reason):
        self.__key = Key(key).value
        self.__revocation = RevoqueAtributte(revocation).value
        self.__reason = ReasonAtributte(reason).value

    def __str__(self):
        """It returns the json corresponding to the AccessRequest"""
        return "AccessRequest:" + json.dumps(self.__dict__)

    @classmethod
    def create_key_from_file(cls, key_file):
        """Class method from creating an instance of RevoqueKey
        from the content of a file according to RF2"""
        revoque = DesactivarJson(key_file).json_content
        return cls(revoque[DesactivarJson.KEY],
                   revoque[DesactivarJson.RENOVATION],
                   revoque[DesactivarJson.REASON])

    def store_revoque(self):
        """Funcion para guardar el revoque"""
        revoque_store = RevoqueStore()
        revoque_store.revoque_key(self)
        emails = revoque_store.load_keys(self)
        return emails

    def emails(self):
        """Funcion para retornar el email"""
        request = KeysJsonStore()
        request_object = request.find_item(self.__key)
        return request_object["_AccessKey__notification_emails"]

    def check_validity(self):
        """Funcion para comprobar que una llave es valida o no"""
        justnow = datetime.utcnow()
        time_stamp = datetime.timestamp(justnow)
        request = KeysJsonStore()
        request_object = request.find_item(self.__key)
        if request_object is None:
            raise AccessManagementException("Error la clave no existe")
        validity = request_object["_AccessKey__expiration_date"]
        if time_stamp > validity != 0:
            raise AccessManagementException("La clave recibida ha caducado")

    @property
    def key(self):
        """Property representing the validity days"""
        return self.__key

    @property
    def revocation(self):
        """Property representing the name and the surname of
        the person who request access to the building"""
        return self.__revocation

    @property
    def reason(self):
        """Property representing the name and the surname of
        the person who request access to the building"""
        return self.__reason

    @key.setter
    def key(self, value):
        """name setter"""
        self.__key = value

    @revocation.setter
    def revocation(self, value):
        self.__revocation = value

    @reason.setter
    def reason(self, value):
        self.__reason = value
