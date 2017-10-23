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


class GetCharactersCharacterIdCalendarEventIdOk(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, date=None, duration=None, event_id=None, importance=None, owner_id=None, owner_name=None, owner_type=None, response=None, text=None, title=None):
        """
        GetCharactersCharacterIdCalendarEventIdOk - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'date': 'datetime',
            'duration': 'int',
            'event_id': 'int',
            'importance': 'int',
            'owner_id': 'int',
            'owner_name': 'str',
            'owner_type': 'str',
            'response': 'str',
            'text': 'str',
            'title': 'str'
        }

        self.attribute_map = {
            'date': 'date',
            'duration': 'duration',
            'event_id': 'event_id',
            'importance': 'importance',
            'owner_id': 'owner_id',
            'owner_name': 'owner_name',
            'owner_type': 'owner_type',
            'response': 'response',
            'text': 'text',
            'title': 'title'
        }

        self._date = date
        self._duration = duration
        self._event_id = event_id
        self._importance = importance
        self._owner_id = owner_id
        self._owner_name = owner_name
        self._owner_type = owner_type
        self._response = response
        self._text = text
        self._title = title

    @property
    def date(self):
        """
        Gets the date of this GetCharactersCharacterIdCalendarEventIdOk.
        date string

        :return: The date of this GetCharactersCharacterIdCalendarEventIdOk.
        :rtype: datetime
        """
        return self._date

    @date.setter
    def date(self, date):
        """
        Sets the date of this GetCharactersCharacterIdCalendarEventIdOk.
        date string

        :param date: The date of this GetCharactersCharacterIdCalendarEventIdOk.
        :type: datetime
        """
        if date is None:
            raise ValueError("Invalid value for `date`, must not be `None`")

        self._date = date

    @property
    def duration(self):
        """
        Gets the duration of this GetCharactersCharacterIdCalendarEventIdOk.
        Length in minutes

        :return: The duration of this GetCharactersCharacterIdCalendarEventIdOk.
        :rtype: int
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        """
        Sets the duration of this GetCharactersCharacterIdCalendarEventIdOk.
        Length in minutes

        :param duration: The duration of this GetCharactersCharacterIdCalendarEventIdOk.
        :type: int
        """
        if duration is None:
            raise ValueError("Invalid value for `duration`, must not be `None`")

        self._duration = duration

    @property
    def event_id(self):
        """
        Gets the event_id of this GetCharactersCharacterIdCalendarEventIdOk.
        event_id integer

        :return: The event_id of this GetCharactersCharacterIdCalendarEventIdOk.
        :rtype: int
        """
        return self._event_id

    @event_id.setter
    def event_id(self, event_id):
        """
        Sets the event_id of this GetCharactersCharacterIdCalendarEventIdOk.
        event_id integer

        :param event_id: The event_id of this GetCharactersCharacterIdCalendarEventIdOk.
        :type: int
        """
        if event_id is None:
            raise ValueError("Invalid value for `event_id`, must not be `None`")

        self._event_id = event_id

    @property
    def importance(self):
        """
        Gets the importance of this GetCharactersCharacterIdCalendarEventIdOk.
        importance integer

        :return: The importance of this GetCharactersCharacterIdCalendarEventIdOk.
        :rtype: int
        """
        return self._importance

    @importance.setter
    def importance(self, importance):
        """
        Sets the importance of this GetCharactersCharacterIdCalendarEventIdOk.
        importance integer

        :param importance: The importance of this GetCharactersCharacterIdCalendarEventIdOk.
        :type: int
        """
        if importance is None:
            raise ValueError("Invalid value for `importance`, must not be `None`")

        self._importance = importance

    @property
    def owner_id(self):
        """
        Gets the owner_id of this GetCharactersCharacterIdCalendarEventIdOk.
        owner_id integer

        :return: The owner_id of this GetCharactersCharacterIdCalendarEventIdOk.
        :rtype: int
        """
        return self._owner_id

    @owner_id.setter
    def owner_id(self, owner_id):
        """
        Sets the owner_id of this GetCharactersCharacterIdCalendarEventIdOk.
        owner_id integer

        :param owner_id: The owner_id of this GetCharactersCharacterIdCalendarEventIdOk.
        :type: int
        """
        if owner_id is None:
            raise ValueError("Invalid value for `owner_id`, must not be `None`")

        self._owner_id = owner_id

    @property
    def owner_name(self):
        """
        Gets the owner_name of this GetCharactersCharacterIdCalendarEventIdOk.
        owner_name string

        :return: The owner_name of this GetCharactersCharacterIdCalendarEventIdOk.
        :rtype: str
        """
        return self._owner_name

    @owner_name.setter
    def owner_name(self, owner_name):
        """
        Sets the owner_name of this GetCharactersCharacterIdCalendarEventIdOk.
        owner_name string

        :param owner_name: The owner_name of this GetCharactersCharacterIdCalendarEventIdOk.
        :type: str
        """
        if owner_name is None:
            raise ValueError("Invalid value for `owner_name`, must not be `None`")

        self._owner_name = owner_name

    @property
    def owner_type(self):
        """
        Gets the owner_type of this GetCharactersCharacterIdCalendarEventIdOk.
        owner_type string

        :return: The owner_type of this GetCharactersCharacterIdCalendarEventIdOk.
        :rtype: str
        """
        return self._owner_type

    @owner_type.setter
    def owner_type(self, owner_type):
        """
        Sets the owner_type of this GetCharactersCharacterIdCalendarEventIdOk.
        owner_type string

        :param owner_type: The owner_type of this GetCharactersCharacterIdCalendarEventIdOk.
        :type: str
        """
        allowed_values = ["eve_server", "corporation", "faction", "character", "alliance"]
        if owner_type not in allowed_values:
            raise ValueError(
                "Invalid value for `owner_type` ({0}), must be one of {1}"
                .format(owner_type, allowed_values)
            )

        self._owner_type = owner_type

    @property
    def response(self):
        """
        Gets the response of this GetCharactersCharacterIdCalendarEventIdOk.
        response string

        :return: The response of this GetCharactersCharacterIdCalendarEventIdOk.
        :rtype: str
        """
        return self._response

    @response.setter
    def response(self, response):
        """
        Sets the response of this GetCharactersCharacterIdCalendarEventIdOk.
        response string

        :param response: The response of this GetCharactersCharacterIdCalendarEventIdOk.
        :type: str
        """
        if response is None:
            raise ValueError("Invalid value for `response`, must not be `None`")

        self._response = response

    @property
    def text(self):
        """
        Gets the text of this GetCharactersCharacterIdCalendarEventIdOk.
        text string

        :return: The text of this GetCharactersCharacterIdCalendarEventIdOk.
        :rtype: str
        """
        return self._text

    @text.setter
    def text(self, text):
        """
        Sets the text of this GetCharactersCharacterIdCalendarEventIdOk.
        text string

        :param text: The text of this GetCharactersCharacterIdCalendarEventIdOk.
        :type: str
        """
        if text is None:
            raise ValueError("Invalid value for `text`, must not be `None`")

        self._text = text

    @property
    def title(self):
        """
        Gets the title of this GetCharactersCharacterIdCalendarEventIdOk.
        title string

        :return: The title of this GetCharactersCharacterIdCalendarEventIdOk.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title of this GetCharactersCharacterIdCalendarEventIdOk.
        title string

        :param title: The title of this GetCharactersCharacterIdCalendarEventIdOk.
        :type: str
        """
        if title is None:
            raise ValueError("Invalid value for `title`, must not be `None`")

        self._title = title

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
        if not isinstance(other, GetCharactersCharacterIdCalendarEventIdOk):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
