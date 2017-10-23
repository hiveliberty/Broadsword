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


class GetCharactersCharacterIdPlanetsPlanetIdOk(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, links=None, pins=None, routes=None):
        """
        GetCharactersCharacterIdPlanetsPlanetIdOk - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'links': 'list[GetCharactersCharacterIdPlanetsPlanetIdLink]',
            'pins': 'list[GetCharactersCharacterIdPlanetsPlanetIdPin]',
            'routes': 'list[GetCharactersCharacterIdPlanetsPlanetIdRoute]'
        }

        self.attribute_map = {
            'links': 'links',
            'pins': 'pins',
            'routes': 'routes'
        }

        self._links = links
        self._pins = pins
        self._routes = routes

    @property
    def links(self):
        """
        Gets the links of this GetCharactersCharacterIdPlanetsPlanetIdOk.
        links array

        :return: The links of this GetCharactersCharacterIdPlanetsPlanetIdOk.
        :rtype: list[GetCharactersCharacterIdPlanetsPlanetIdLink]
        """
        return self._links

    @links.setter
    def links(self, links):
        """
        Sets the links of this GetCharactersCharacterIdPlanetsPlanetIdOk.
        links array

        :param links: The links of this GetCharactersCharacterIdPlanetsPlanetIdOk.
        :type: list[GetCharactersCharacterIdPlanetsPlanetIdLink]
        """
        if links is None:
            raise ValueError("Invalid value for `links`, must not be `None`")

        self._links = links

    @property
    def pins(self):
        """
        Gets the pins of this GetCharactersCharacterIdPlanetsPlanetIdOk.
        pins array

        :return: The pins of this GetCharactersCharacterIdPlanetsPlanetIdOk.
        :rtype: list[GetCharactersCharacterIdPlanetsPlanetIdPin]
        """
        return self._pins

    @pins.setter
    def pins(self, pins):
        """
        Sets the pins of this GetCharactersCharacterIdPlanetsPlanetIdOk.
        pins array

        :param pins: The pins of this GetCharactersCharacterIdPlanetsPlanetIdOk.
        :type: list[GetCharactersCharacterIdPlanetsPlanetIdPin]
        """
        if pins is None:
            raise ValueError("Invalid value for `pins`, must not be `None`")

        self._pins = pins

    @property
    def routes(self):
        """
        Gets the routes of this GetCharactersCharacterIdPlanetsPlanetIdOk.
        routes array

        :return: The routes of this GetCharactersCharacterIdPlanetsPlanetIdOk.
        :rtype: list[GetCharactersCharacterIdPlanetsPlanetIdRoute]
        """
        return self._routes

    @routes.setter
    def routes(self, routes):
        """
        Sets the routes of this GetCharactersCharacterIdPlanetsPlanetIdOk.
        routes array

        :param routes: The routes of this GetCharactersCharacterIdPlanetsPlanetIdOk.
        :type: list[GetCharactersCharacterIdPlanetsPlanetIdRoute]
        """
        if routes is None:
            raise ValueError("Invalid value for `routes`, must not be `None`")

        self._routes = routes

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
        if not isinstance(other, GetCharactersCharacterIdPlanetsPlanetIdOk):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
