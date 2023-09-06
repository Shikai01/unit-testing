"""Clase encargada de que la razon introducida no es mayor a 100"""
from .attribute import Attribute


class ReasonAtributte(Attribute):
    """Class for validating reason in secure_all"""

    # pylint: disable=too-few-public-methods

    def __init__(self, attr_value):
        self._validation_pattern = r'.{1,100}'
        self._error_message = "Revoque invalid"
        self._attr_value = self._validate(attr_value)
