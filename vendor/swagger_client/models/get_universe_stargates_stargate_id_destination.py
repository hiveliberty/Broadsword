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


class GetUniverseStargatesStargateIdDestination(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, stargate_id=None, system_id=None):
        """
        GetUniverseStargatesStargateIdDestination - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'stargate_id': 'int',
            'system_id': 'int'
        }

        self.attribute_map = {
            'stargate_id': 'stargate_id',
            'system_id': 'system_id'
        }

        self._stargate_id = stargate_id
        self._system_id = system_id

    @property
    def stargate_id(self):
        """
        Gets the stargate_id of this GetUniverseStargatesStargateIdDestination.
        The stargate this stargate connects to

        :return: The stargate_id of this GetUniverseStargatesStargateIdDestination.
        :rtype: int
        """
        return self._stargate_id

    @stargate_id.setter
    def stargate_id(self, stargate_id):
        """
        Sets the stargate_id of this GetUniverseStargatesStargateIdDestination.
        The stargate this stargate connects to

        :param stargate_id: The stargate_id of this GetUniverseStargatesStargateIdDestination.
        :type: int
        """
        if stargate_id is None:
            raise ValueError("Invalid value for `stargate_id`, must not be `None`")

        self._stargate_id = stargate_id

    @property
    def system_id(self):
        """
        Gets the system_id of this GetUniverseStargatesStargateIdDestination.
        The solar system this stargate connects to

        :return: The system_id of this GetUniverseStargatesStargateIdDestination.
        :rtype: int
        """
        return self._system_id

    @system_id.setter
    def system_id(self, system_id):
        """
        Sets the system_id of this GetUniverseStargatesStargateIdDestination.
        The solar system this stargate connects to

        :param system_id: The system_id of this GetUniverseStargatesStargateIdDestination.
        :type: int
        """
        if system_id is None:
            raise ValueError("Invalid value for `system_id`, must not be `None`")

        self._system_id = system_id

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
        if not isinstance(other, GetUniverseStargatesStargateIdDestination):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
