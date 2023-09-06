"""Funcion para eliminar un key"""
import json
from secure_all.storage.json_store import JsonStore
from secure_all.exception.access_management_exception import AccessManagementException
from secure_all.cfg.access_manager_config import JSON_FILES_PATH


class RevoqueStore:
    """Extends JsonStore """

    class __RevoqueStore(JsonStore):
        # pylint: disable=invalid-name
        ID_FIELD = "_AccessKey__key"
        INVALID_ITEM = "Invalid item to be stored as a revoque"
        KEY_ALREDY_REVOQUED = "key already Revoqued"

        _FILE_PATH = JSON_FILES_PATH + "RevoqueKeys.json"
        _ID_FIELD = ID_FIELD

        def revoque_key(self, item):
            """Implementing the restrictions related to avoid duplicated keys"""
            _FILE_PATH = JSON_FILES_PATH + "RevoqueKeys.json"
            # pylint: disable=import-outside-toplevel,cyclic-import
            from secure_all.data.access_revoqued import TypeAccessRevoqued

            if not isinstance(item, TypeAccessRevoqued):
                raise AccessManagementException(self.INVALID_ITEM)

            if not self.find_item(item.key) is None:
                raise AccessManagementException(self.KEY_ALREDY_REVOQUED)

            self.load_store()
            self.search_revoque(item.key)
            datos = {"_AccessKey__key": item.key}
            self._data_list.append(datos)
            self.save_store()

        def search_revoque(self, key):
            """Buscar si la llave ya fue eliminada o no"""
            if not self.find_item(key) is None:
                raise AccessManagementException(self.KEY_ALREDY_REVOQUED)

        def cambiar_datos(self):
            """Buscar dentro de storeKeys la llave"""
            camino = JSON_FILES_PATH + "storeKeys.json"
            try:
                with open(camino, "r", encoding="utf-8", newline="") as file:
                    self._data_list = json.load(file)
            except FileNotFoundError as ex:
                self._data_list = []
            except json.JSONDecodeError as ex:
                raise AccessManagementException("JSON Decode Error - Wrong JSON Format") from ex

        def load_keys(self, dato):
            """Obtener los emails del key"""
            self.cambiar_datos()
            for item in self._data_list:
                if item["_AccessKey__key"] == dato.key:
                    return item["_AccessKey__notification_emails"]
            return None

    __instance = None

    def __new__(cls):
        if not RevoqueStore.__instance:
            RevoqueStore.__instance = RevoqueStore.__RevoqueStore()
        return RevoqueStore.__instance

    def __getattr__(self, nombre):
        return getattr(self.__instance, nombre)

    def __setattr__(self, nombre, valor):
        return setattr(self.__instance, nombre, valor)
