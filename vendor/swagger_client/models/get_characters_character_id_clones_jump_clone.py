# coding: utf-8

"""
    EVE Swagger Interface

    An OpenAPI for EVE Online

    OpenAPI spec version: 0.7.3
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class GetCharactersCharacterIdClonesJumpClone(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'jump_clone_id': 'int',
        'name': 'str',
        'location_id': 'int',
        'location_type': 'str',
        'implants': 'list[int]'
    }

    attribute_map = {
        'jump_clone_id': 'jump_clone_id',
        'name': 'name',
        'location_id': 'location_id',
        'location_type': 'location_type',
        'implants': 'implants'
    }

    def __init__(self, jump_clone_id=None, name=None, location_id=None, location_type=None, implants=None):
        """
        GetCharactersCharacterIdClonesJumpClone - a model defined in Swagger
        """

        self._jump_clone_id = None
        self._name = None
        self._location_id = None
        self._location_type = None
        self._implants = None
        self.discriminator = None

        self.jump_clone_id = jump_clone_id
        if name is not None:
          self.name = name
        self.location_id = location_id
        self.location_type = location_type
        self.implants = implants

    @property
    def jump_clone_id(self):
        """
        Gets the jump_clone_id of this GetCharactersCharacterIdClonesJumpClone.
        jump_clone_id integer

        :return: The jump_clone_id of this GetCharactersCharacterIdClonesJumpClone.
        :rtype: int
        """
        return self._jump_clone_id

    @jump_clone_id.setter
    def jump_clone_id(self, jump_clone_id):
        """
        Sets the jump_clone_id of this GetCharactersCharacterIdClonesJumpClone.
        jump_clone_id integer

        :param jump_clone_id: The jump_clone_id of this GetCharactersCharacterIdClonesJumpClone.
        :type: int
        """
        if jump_clone_id is None:
            raise ValueError("Invalid value for `jump_clone_id`, must not be `None`")

        self._jump_clone_id = jump_clone_id

    @property
    def name(self):
        """
        Gets the name of this GetCharactersCharacterIdClonesJumpClone.
        name string

        :return: The name of this GetCharactersCharacterIdClonesJumpClone.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this GetCharactersCharacterIdClonesJumpClone.
        name string

        :param name: The name of this GetCharactersCharacterIdClonesJumpClone.
        :type: str
        """

        self._name = name

    @property
    def location_id(self):
        """
        Gets the location_id of this GetCharactersCharacterIdClonesJumpClone.
        location_id integer

        :return: The location_id of this GetCharactersCharacterIdClonesJumpClone.
        :rtype: int
        """
        return self._location_id

    @location_id.setter
    def location_id(self, location_id):
        """
        Sets the location_id of this GetCharactersCharacterIdClonesJumpClone.
        location_id integer

        :param location_id: The location_id of this GetCharactersCharacterIdClonesJumpClone.
        :type: int
        """
        if location_id is None:
            raise ValueError("Invalid value for `location_id`, must not be `None`")

        self._location_id = location_id

    @property
    def location_type(self):
        """
        Gets the location_type of this GetCharactersCharacterIdClonesJumpClone.
        location_type string

        :return: The location_type of this GetCharactersCharacterIdClonesJumpClone.
        :rtype: str
        """
        return self._location_type

    @location_type.setter
    def location_type(self, location_type):
        """
        Sets the location_type of this GetCharactersCharacterIdClonesJumpClone.
        location_type string

        :param location_type: The location_type of this GetCharactersCharacterIdClonesJumpClone.
        :type: str
        """
        if location_type is None:
            raise ValueError("Invalid value for `location_type`, must not be `None`")
        allowed_values = ["station", "structure"]
        if location_type not in allowed_values:
            raise ValueError(
                "Invalid value for `location_type` ({0}), must be one of {1}"
                .format(location_type, allowed_values)
            )

        self._location_type = location_type

    @property
    def implants(self):
        """
        Gets the implants of this GetCharactersCharacterIdClonesJumpClone.
        implants array

        :return: The implants of this GetCharactersCharacterIdClonesJumpClone.
        :rtype: list[int]
        """
        return self._implants

    @implants.setter
    def implants(self, implants):
        """
        Sets the implants of this GetCharactersCharacterIdClonesJumpClone.
        implants array

        :param implants: The implants of this GetCharactersCharacterIdClonesJumpClone.
        :type: list[int]
        """
        if implants is None:
            raise ValueError("Invalid value for `implants`, must not be `None`")

        self._implants = implants

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
        if not isinstance(other, GetCharactersCharacterIdClonesJumpClone):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
