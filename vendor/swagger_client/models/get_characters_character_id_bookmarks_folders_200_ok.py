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


class GetCharactersCharacterIdBookmarksFolders200Ok(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, folder_id=None, name=None, owner_id=None):
        """
        GetCharactersCharacterIdBookmarksFolders200Ok - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'folder_id': 'int',
            'name': 'str',
            'owner_id': 'int'
        }

        self.attribute_map = {
            'folder_id': 'folder_id',
            'name': 'name',
            'owner_id': 'owner_id'
        }

        self._folder_id = folder_id
        self._name = name
        self._owner_id = owner_id

    @property
    def folder_id(self):
        """
        Gets the folder_id of this GetCharactersCharacterIdBookmarksFolders200Ok.
        folder_id integer

        :return: The folder_id of this GetCharactersCharacterIdBookmarksFolders200Ok.
        :rtype: int
        """
        return self._folder_id

    @folder_id.setter
    def folder_id(self, folder_id):
        """
        Sets the folder_id of this GetCharactersCharacterIdBookmarksFolders200Ok.
        folder_id integer

        :param folder_id: The folder_id of this GetCharactersCharacterIdBookmarksFolders200Ok.
        :type: int
        """

        self._folder_id = folder_id

    @property
    def name(self):
        """
        Gets the name of this GetCharactersCharacterIdBookmarksFolders200Ok.
        name string

        :return: The name of this GetCharactersCharacterIdBookmarksFolders200Ok.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this GetCharactersCharacterIdBookmarksFolders200Ok.
        name string

        :param name: The name of this GetCharactersCharacterIdBookmarksFolders200Ok.
        :type: str
        """

        self._name = name

    @property
    def owner_id(self):
        """
        Gets the owner_id of this GetCharactersCharacterIdBookmarksFolders200Ok.
        owner_id integer

        :return: The owner_id of this GetCharactersCharacterIdBookmarksFolders200Ok.
        :rtype: int
        """
        return self._owner_id

    @owner_id.setter
    def owner_id(self, owner_id):
        """
        Sets the owner_id of this GetCharactersCharacterIdBookmarksFolders200Ok.
        owner_id integer

        :param owner_id: The owner_id of this GetCharactersCharacterIdBookmarksFolders200Ok.
        :type: int
        """

        self._owner_id = owner_id

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
        if not isinstance(other, GetCharactersCharacterIdBookmarksFolders200Ok):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
