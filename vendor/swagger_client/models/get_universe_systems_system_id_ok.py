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


class GetUniverseSystemsSystemIdOk(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, constellation_id=None, name=None, planets=None, position=None, security_class=None, security_status=None, star_id=None, stargates=None, stations=None, system_id=None):
        """
        GetUniverseSystemsSystemIdOk - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'constellation_id': 'int',
            'name': 'str',
            'planets': 'list[GetUniverseSystemsSystemIdPlanet]',
            'position': 'GetUniverseSystemsSystemIdPosition',
            'security_class': 'str',
            'security_status': 'float',
            'star_id': 'int',
            'stargates': 'list[int]',
            'stations': 'list[int]',
            'system_id': 'int'
        }

        self.attribute_map = {
            'constellation_id': 'constellation_id',
            'name': 'name',
            'planets': 'planets',
            'position': 'position',
            'security_class': 'security_class',
            'security_status': 'security_status',
            'star_id': 'star_id',
            'stargates': 'stargates',
            'stations': 'stations',
            'system_id': 'system_id'
        }

        self._constellation_id = constellation_id
        self._name = name
        self._planets = planets
        self._position = position
        self._security_class = security_class
        self._security_status = security_status
        self._star_id = star_id
        self._stargates = stargates
        self._stations = stations
        self._system_id = system_id

    @property
    def constellation_id(self):
        """
        Gets the constellation_id of this GetUniverseSystemsSystemIdOk.
        The constellation this solar system is in

        :return: The constellation_id of this GetUniverseSystemsSystemIdOk.
        :rtype: int
        """
        return self._constellation_id

    @constellation_id.setter
    def constellation_id(self, constellation_id):
        """
        Sets the constellation_id of this GetUniverseSystemsSystemIdOk.
        The constellation this solar system is in

        :param constellation_id: The constellation_id of this GetUniverseSystemsSystemIdOk.
        :type: int
        """
        if constellation_id is None:
            raise ValueError("Invalid value for `constellation_id`, must not be `None`")

        self._constellation_id = constellation_id

    @property
    def name(self):
        """
        Gets the name of this GetUniverseSystemsSystemIdOk.
        name string

        :return: The name of this GetUniverseSystemsSystemIdOk.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this GetUniverseSystemsSystemIdOk.
        name string

        :param name: The name of this GetUniverseSystemsSystemIdOk.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def planets(self):
        """
        Gets the planets of this GetUniverseSystemsSystemIdOk.
        planets array

        :return: The planets of this GetUniverseSystemsSystemIdOk.
        :rtype: list[GetUniverseSystemsSystemIdPlanet]
        """
        return self._planets

    @planets.setter
    def planets(self, planets):
        """
        Sets the planets of this GetUniverseSystemsSystemIdOk.
        planets array

        :param planets: The planets of this GetUniverseSystemsSystemIdOk.
        :type: list[GetUniverseSystemsSystemIdPlanet]
        """
        if planets is None:
            raise ValueError("Invalid value for `planets`, must not be `None`")

        self._planets = planets

    @property
    def position(self):
        """
        Gets the position of this GetUniverseSystemsSystemIdOk.

        :return: The position of this GetUniverseSystemsSystemIdOk.
        :rtype: GetUniverseSystemsSystemIdPosition
        """
        return self._position

    @position.setter
    def position(self, position):
        """
        Sets the position of this GetUniverseSystemsSystemIdOk.

        :param position: The position of this GetUniverseSystemsSystemIdOk.
        :type: GetUniverseSystemsSystemIdPosition
        """

        self._position = position

    @property
    def security_class(self):
        """
        Gets the security_class of this GetUniverseSystemsSystemIdOk.
        security_class string

        :return: The security_class of this GetUniverseSystemsSystemIdOk.
        :rtype: str
        """
        return self._security_class

    @security_class.setter
    def security_class(self, security_class):
        """
        Sets the security_class of this GetUniverseSystemsSystemIdOk.
        security_class string

        :param security_class: The security_class of this GetUniverseSystemsSystemIdOk.
        :type: str
        """

        self._security_class = security_class

    @property
    def security_status(self):
        """
        Gets the security_status of this GetUniverseSystemsSystemIdOk.
        security_status number

        :return: The security_status of this GetUniverseSystemsSystemIdOk.
        :rtype: float
        """
        return self._security_status

    @security_status.setter
    def security_status(self, security_status):
        """
        Sets the security_status of this GetUniverseSystemsSystemIdOk.
        security_status number

        :param security_status: The security_status of this GetUniverseSystemsSystemIdOk.
        :type: float
        """
        if security_status is None:
            raise ValueError("Invalid value for `security_status`, must not be `None`")

        self._security_status = security_status

    @property
    def star_id(self):
        """
        Gets the star_id of this GetUniverseSystemsSystemIdOk.
        star_id integer

        :return: The star_id of this GetUniverseSystemsSystemIdOk.
        :rtype: int
        """
        return self._star_id

    @star_id.setter
    def star_id(self, star_id):
        """
        Sets the star_id of this GetUniverseSystemsSystemIdOk.
        star_id integer

        :param star_id: The star_id of this GetUniverseSystemsSystemIdOk.
        :type: int
        """
        if star_id is None:
            raise ValueError("Invalid value for `star_id`, must not be `None`")

        self._star_id = star_id

    @property
    def stargates(self):
        """
        Gets the stargates of this GetUniverseSystemsSystemIdOk.
        stargates array

        :return: The stargates of this GetUniverseSystemsSystemIdOk.
        :rtype: list[int]
        """
        return self._stargates

    @stargates.setter
    def stargates(self, stargates):
        """
        Sets the stargates of this GetUniverseSystemsSystemIdOk.
        stargates array

        :param stargates: The stargates of this GetUniverseSystemsSystemIdOk.
        :type: list[int]
        """

        self._stargates = stargates

    @property
    def stations(self):
        """
        Gets the stations of this GetUniverseSystemsSystemIdOk.
        stations array

        :return: The stations of this GetUniverseSystemsSystemIdOk.
        :rtype: list[int]
        """
        return self._stations

    @stations.setter
    def stations(self, stations):
        """
        Sets the stations of this GetUniverseSystemsSystemIdOk.
        stations array

        :param stations: The stations of this GetUniverseSystemsSystemIdOk.
        :type: list[int]
        """

        self._stations = stations

    @property
    def system_id(self):
        """
        Gets the system_id of this GetUniverseSystemsSystemIdOk.
        system_id integer

        :return: The system_id of this GetUniverseSystemsSystemIdOk.
        :rtype: int
        """
        return self._system_id

    @system_id.setter
    def system_id(self, system_id):
        """
        Sets the system_id of this GetUniverseSystemsSystemIdOk.
        system_id integer

        :param system_id: The system_id of this GetUniverseSystemsSystemIdOk.
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
        if not isinstance(other, GetUniverseSystemsSystemIdOk):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
