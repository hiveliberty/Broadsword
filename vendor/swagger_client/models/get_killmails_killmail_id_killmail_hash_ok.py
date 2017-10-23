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


class GetKillmailsKillmailIdKillmailHashOk(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, attackers=None, killmail_id=None, killmail_time=None, moon_id=None, solar_system_id=None, victim=None, war_id=None):
        """
        GetKillmailsKillmailIdKillmailHashOk - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'attackers': 'list[GetKillmailsKillmailIdKillmailHashAttacker]',
            'killmail_id': 'int',
            'killmail_time': 'datetime',
            'moon_id': 'int',
            'solar_system_id': 'int',
            'victim': 'GetKillmailsKillmailIdKillmailHashVictim',
            'war_id': 'int'
        }

        self.attribute_map = {
            'attackers': 'attackers',
            'killmail_id': 'killmail_id',
            'killmail_time': 'killmail_time',
            'moon_id': 'moon_id',
            'solar_system_id': 'solar_system_id',
            'victim': 'victim',
            'war_id': 'war_id'
        }

        self._attackers = attackers
        self._killmail_id = killmail_id
        self._killmail_time = killmail_time
        self._moon_id = moon_id
        self._solar_system_id = solar_system_id
        self._victim = victim
        self._war_id = war_id

    @property
    def attackers(self):
        """
        Gets the attackers of this GetKillmailsKillmailIdKillmailHashOk.
        attackers array

        :return: The attackers of this GetKillmailsKillmailIdKillmailHashOk.
        :rtype: list[GetKillmailsKillmailIdKillmailHashAttacker]
        """
        return self._attackers

    @attackers.setter
    def attackers(self, attackers):
        """
        Sets the attackers of this GetKillmailsKillmailIdKillmailHashOk.
        attackers array

        :param attackers: The attackers of this GetKillmailsKillmailIdKillmailHashOk.
        :type: list[GetKillmailsKillmailIdKillmailHashAttacker]
        """
        if attackers is None:
            raise ValueError("Invalid value for `attackers`, must not be `None`")

        self._attackers = attackers

    @property
    def killmail_id(self):
        """
        Gets the killmail_id of this GetKillmailsKillmailIdKillmailHashOk.
        ID of the killmail

        :return: The killmail_id of this GetKillmailsKillmailIdKillmailHashOk.
        :rtype: int
        """
        return self._killmail_id

    @killmail_id.setter
    def killmail_id(self, killmail_id):
        """
        Sets the killmail_id of this GetKillmailsKillmailIdKillmailHashOk.
        ID of the killmail

        :param killmail_id: The killmail_id of this GetKillmailsKillmailIdKillmailHashOk.
        :type: int
        """
        if killmail_id is None:
            raise ValueError("Invalid value for `killmail_id`, must not be `None`")

        self._killmail_id = killmail_id

    @property
    def killmail_time(self):
        """
        Gets the killmail_time of this GetKillmailsKillmailIdKillmailHashOk.
        Time that the victim was killed and the killmail generated 

        :return: The killmail_time of this GetKillmailsKillmailIdKillmailHashOk.
        :rtype: datetime
        """
        return self._killmail_time

    @killmail_time.setter
    def killmail_time(self, killmail_time):
        """
        Sets the killmail_time of this GetKillmailsKillmailIdKillmailHashOk.
        Time that the victim was killed and the killmail generated 

        :param killmail_time: The killmail_time of this GetKillmailsKillmailIdKillmailHashOk.
        :type: datetime
        """
        if killmail_time is None:
            raise ValueError("Invalid value for `killmail_time`, must not be `None`")

        self._killmail_time = killmail_time

    @property
    def moon_id(self):
        """
        Gets the moon_id of this GetKillmailsKillmailIdKillmailHashOk.
        Moon if the kill took place at one

        :return: The moon_id of this GetKillmailsKillmailIdKillmailHashOk.
        :rtype: int
        """
        return self._moon_id

    @moon_id.setter
    def moon_id(self, moon_id):
        """
        Sets the moon_id of this GetKillmailsKillmailIdKillmailHashOk.
        Moon if the kill took place at one

        :param moon_id: The moon_id of this GetKillmailsKillmailIdKillmailHashOk.
        :type: int
        """

        self._moon_id = moon_id

    @property
    def solar_system_id(self):
        """
        Gets the solar_system_id of this GetKillmailsKillmailIdKillmailHashOk.
        Solar system that the kill took place in 

        :return: The solar_system_id of this GetKillmailsKillmailIdKillmailHashOk.
        :rtype: int
        """
        return self._solar_system_id

    @solar_system_id.setter
    def solar_system_id(self, solar_system_id):
        """
        Sets the solar_system_id of this GetKillmailsKillmailIdKillmailHashOk.
        Solar system that the kill took place in 

        :param solar_system_id: The solar_system_id of this GetKillmailsKillmailIdKillmailHashOk.
        :type: int
        """
        if solar_system_id is None:
            raise ValueError("Invalid value for `solar_system_id`, must not be `None`")

        self._solar_system_id = solar_system_id

    @property
    def victim(self):
        """
        Gets the victim of this GetKillmailsKillmailIdKillmailHashOk.

        :return: The victim of this GetKillmailsKillmailIdKillmailHashOk.
        :rtype: GetKillmailsKillmailIdKillmailHashVictim
        """
        return self._victim

    @victim.setter
    def victim(self, victim):
        """
        Sets the victim of this GetKillmailsKillmailIdKillmailHashOk.

        :param victim: The victim of this GetKillmailsKillmailIdKillmailHashOk.
        :type: GetKillmailsKillmailIdKillmailHashVictim
        """

        self._victim = victim

    @property
    def war_id(self):
        """
        Gets the war_id of this GetKillmailsKillmailIdKillmailHashOk.
        War if the killmail is generated in relation to an official war 

        :return: The war_id of this GetKillmailsKillmailIdKillmailHashOk.
        :rtype: int
        """
        return self._war_id

    @war_id.setter
    def war_id(self, war_id):
        """
        Sets the war_id of this GetKillmailsKillmailIdKillmailHashOk.
        War if the killmail is generated in relation to an official war 

        :param war_id: The war_id of this GetKillmailsKillmailIdKillmailHashOk.
        :type: int
        """

        self._war_id = war_id

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
        if not isinstance(other, GetKillmailsKillmailIdKillmailHashOk):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
