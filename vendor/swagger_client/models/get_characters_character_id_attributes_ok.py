# coding: utf-8

"""
    EVE Swagger Interface

    An OpenAPI for EVE Online

    OpenAPI spec version: 0.6.2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class GetCharactersCharacterIdAttributesOk(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, accrued_remap_cooldown_date=None, bonus_remaps=None, charisma=None, intelligence=None, last_remap_date=None, memory=None, perception=None, willpower=None):
        """
        GetCharactersCharacterIdAttributesOk - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'accrued_remap_cooldown_date': 'datetime',
            'bonus_remaps': 'int',
            'charisma': 'int',
            'intelligence': 'int',
            'last_remap_date': 'datetime',
            'memory': 'int',
            'perception': 'int',
            'willpower': 'int'
        }

        self.attribute_map = {
            'accrued_remap_cooldown_date': 'accrued_remap_cooldown_date',
            'bonus_remaps': 'bonus_remaps',
            'charisma': 'charisma',
            'intelligence': 'intelligence',
            'last_remap_date': 'last_remap_date',
            'memory': 'memory',
            'perception': 'perception',
            'willpower': 'willpower'
        }

        self._accrued_remap_cooldown_date = accrued_remap_cooldown_date
        self._bonus_remaps = bonus_remaps
        self._charisma = charisma
        self._intelligence = intelligence
        self._last_remap_date = last_remap_date
        self._memory = memory
        self._perception = perception
        self._willpower = willpower

    @property
    def accrued_remap_cooldown_date(self):
        """
        Gets the accrued_remap_cooldown_date of this GetCharactersCharacterIdAttributesOk.
        Neural remapping cooldown after a character uses remap accrued over time

        :return: The accrued_remap_cooldown_date of this GetCharactersCharacterIdAttributesOk.
        :rtype: datetime
        """
        return self._accrued_remap_cooldown_date

    @accrued_remap_cooldown_date.setter
    def accrued_remap_cooldown_date(self, accrued_remap_cooldown_date):
        """
        Sets the accrued_remap_cooldown_date of this GetCharactersCharacterIdAttributesOk.
        Neural remapping cooldown after a character uses remap accrued over time

        :param accrued_remap_cooldown_date: The accrued_remap_cooldown_date of this GetCharactersCharacterIdAttributesOk.
        :type: datetime
        """

        self._accrued_remap_cooldown_date = accrued_remap_cooldown_date

    @property
    def bonus_remaps(self):
        """
        Gets the bonus_remaps of this GetCharactersCharacterIdAttributesOk.
        Number of available bonus character neural remaps

        :return: The bonus_remaps of this GetCharactersCharacterIdAttributesOk.
        :rtype: int
        """
        return self._bonus_remaps

    @bonus_remaps.setter
    def bonus_remaps(self, bonus_remaps):
        """
        Sets the bonus_remaps of this GetCharactersCharacterIdAttributesOk.
        Number of available bonus character neural remaps

        :param bonus_remaps: The bonus_remaps of this GetCharactersCharacterIdAttributesOk.
        :type: int
        """

        self._bonus_remaps = bonus_remaps

    @property
    def charisma(self):
        """
        Gets the charisma of this GetCharactersCharacterIdAttributesOk.
        charisma integer

        :return: The charisma of this GetCharactersCharacterIdAttributesOk.
        :rtype: int
        """
        return self._charisma

    @charisma.setter
    def charisma(self, charisma):
        """
        Sets the charisma of this GetCharactersCharacterIdAttributesOk.
        charisma integer

        :param charisma: The charisma of this GetCharactersCharacterIdAttributesOk.
        :type: int
        """
        if charisma is None:
            raise ValueError("Invalid value for `charisma`, must not be `None`")

        self._charisma = charisma

    @property
    def intelligence(self):
        """
        Gets the intelligence of this GetCharactersCharacterIdAttributesOk.
        intelligence integer

        :return: The intelligence of this GetCharactersCharacterIdAttributesOk.
        :rtype: int
        """
        return self._intelligence

    @intelligence.setter
    def intelligence(self, intelligence):
        """
        Sets the intelligence of this GetCharactersCharacterIdAttributesOk.
        intelligence integer

        :param intelligence: The intelligence of this GetCharactersCharacterIdAttributesOk.
        :type: int
        """
        if intelligence is None:
            raise ValueError("Invalid value for `intelligence`, must not be `None`")

        self._intelligence = intelligence

    @property
    def last_remap_date(self):
        """
        Gets the last_remap_date of this GetCharactersCharacterIdAttributesOk.
        Datetime of last neural remap, including usage of bonus remaps

        :return: The last_remap_date of this GetCharactersCharacterIdAttributesOk.
        :rtype: datetime
        """
        return self._last_remap_date

    @last_remap_date.setter
    def last_remap_date(self, last_remap_date):
        """
        Sets the last_remap_date of this GetCharactersCharacterIdAttributesOk.
        Datetime of last neural remap, including usage of bonus remaps

        :param last_remap_date: The last_remap_date of this GetCharactersCharacterIdAttributesOk.
        :type: datetime
        """

        self._last_remap_date = last_remap_date

    @property
    def memory(self):
        """
        Gets the memory of this GetCharactersCharacterIdAttributesOk.
        memory integer

        :return: The memory of this GetCharactersCharacterIdAttributesOk.
        :rtype: int
        """
        return self._memory

    @memory.setter
    def memory(self, memory):
        """
        Sets the memory of this GetCharactersCharacterIdAttributesOk.
        memory integer

        :param memory: The memory of this GetCharactersCharacterIdAttributesOk.
        :type: int
        """
        if memory is None:
            raise ValueError("Invalid value for `memory`, must not be `None`")

        self._memory = memory

    @property
    def perception(self):
        """
        Gets the perception of this GetCharactersCharacterIdAttributesOk.
        perception integer

        :return: The perception of this GetCharactersCharacterIdAttributesOk.
        :rtype: int
        """
        return self._perception

    @perception.setter
    def perception(self, perception):
        """
        Sets the perception of this GetCharactersCharacterIdAttributesOk.
        perception integer

        :param perception: The perception of this GetCharactersCharacterIdAttributesOk.
        :type: int
        """
        if perception is None:
            raise ValueError("Invalid value for `perception`, must not be `None`")

        self._perception = perception

    @property
    def willpower(self):
        """
        Gets the willpower of this GetCharactersCharacterIdAttributesOk.
        willpower integer

        :return: The willpower of this GetCharactersCharacterIdAttributesOk.
        :rtype: int
        """
        return self._willpower

    @willpower.setter
    def willpower(self, willpower):
        """
        Sets the willpower of this GetCharactersCharacterIdAttributesOk.
        willpower integer

        :param willpower: The willpower of this GetCharactersCharacterIdAttributesOk.
        :type: int
        """
        if willpower is None:
            raise ValueError("Invalid value for `willpower`, must not be `None`")

        self._willpower = willpower

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, GetCharactersCharacterIdAttributesOk):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other