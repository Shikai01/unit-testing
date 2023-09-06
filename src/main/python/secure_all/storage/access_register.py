"""Class for Access Register"""

from datetime import datetime
from secure_all.storage.json_store import JsonStore
from secure_all.exception.access_management_exception import AccessManagementException
from secure_all.cfg.access_manager_config import JSON_FILES_PATH


class AccessRegister:
    """Clase para guardar los registros"""
    class __AccessRegister(JsonStore):
        # pylint: disable=invalid-name
        """-Se define el path a donde se guardan los items
        -Se define un mensaje de error por si no se puede guardar el item """
        _FILE_PATH = JSON_FILES_PATH + "storeAccess.json"
        INVALID_ITEM = "Inavalid item to be stored"

        def save_access(self, item):
            """busco instancia de item en AccessKey
            y le doy etiqueta para agregarlo y guardarlo posteriormente
            -se guarda el access, siendo el tiempo con el código"""
            # pylint: disable=import-outside-toplevel,cyclic-import
            justnow = datetime.utcnow()
            actual_time = datetime.timestamp(justnow)

            from secure_all.data.access_key import AccessKey
            if not isinstance(item, AccessKey):
                raise AccessManagementException(self.INVALID_ITEM)
            self.load_store()
            datos = {"Time": actual_time, "Access_Code": item.access_code}
            self._data_list.append(datos)
            self.save_store()

    __instance = None

    def __new__(cls):
        if not AccessRegister.__instance:
            AccessRegister.__instance = AccessRegister.__AccessRegister()
        return AccessRegister.__instance
