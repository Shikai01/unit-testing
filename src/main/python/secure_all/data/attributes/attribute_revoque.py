"""Class for checking the revoque"""
from .attribute import Attribute


class RevoqueAtributte(Attribute):
    """Class for validating the access code values in secure_all"""

    # pylint: disable=too-few-public-methods

    def __init__(self, attr_value):
        self._validation_pattern = r'(Temporal|Final)'
        self._error_message = "Revoque invalid"
        self._attr_value = self._validate(attr_value)
