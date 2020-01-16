# coding: utf-8

# (C) Copyright IBM Corp. 2019, 2020.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
The IBM Watson&trade; Assistant service combines machine learning, natural language
understanding, and an integrated dialog editor to create conversation flows between your
apps and your users.
The Assistant v2 API provides runtime methods your client application can use to send user
input to an assistant and receive a response.
"""

import json
from ibm_cloud_sdk_core.authenticators.authenticator import Authenticator
from .common import get_sdk_headers
from enum import Enum
from ibm_cloud_sdk_core import BaseService
from ibm_cloud_sdk_core import get_authenticator_from_environment
from typing import Dict
from typing import List

##############################################################################
# Service
##############################################################################


class AssistantV2(BaseService):
    """The Assistant V2 service."""

    DEFAULT_SERVICE_URL = 'https://gateway.watsonplatform.net/assistant/api'
    DEFAULT_SERVICE_NAME = 'conversation'

    def __init__(
            self,
            version: str,
            authenticator: Authenticator = None,
            service_name: str = DEFAULT_SERVICE_NAME,
    ) -> None:
        """
        Construct a new client for the Assistant service.

        :param str version: The API version date to use with the service, in
               "YYYY-MM-DD" format. Whenever the API is changed in a backwards
               incompatible way, a new minor version of the API is released.
               The service uses the API version for the date you specify, or
               the most recent version before that date. Note that you should
               not programmatically specify the current date at runtime, in
               case the API has been updated since your application's release.
               Instead, specify a version date that is compatible with your
               application, and don't change it until your application is
               ready for a later version.

        :param Authenticator authenticator: The authenticator specifies the authentication mechanism.
               Get up to date information from https://github.com/IBM/python-sdk-core/blob/master/README.md
               about initializing the authenticator of your choice.
        """
        if not authenticator:
            authenticator = get_authenticator_from_environment(service_name)
        BaseService.__init__(self,
                             service_url=self.DEFAULT_SERVICE_URL,
                             authenticator=authenticator,
                             disable_ssl_verification=False)
        self.version = version
        self.configure_service(service_name)

    #########################
    # Sessions
    #########################

    def create_session(self, assistant_id: str, **kwargs) -> 'DetailedResponse':
        """
        Create a session.

        Create a new session. A session is used to send user input to a skill and receive
        responses. It also maintains the state of the conversation. A session persists
        until it is deleted, or until it times out because of inactivity. (For more
        information, see the
        [documentation](https://cloud.ibm.com/docs/services/assistant?topic=assistant-assistant-settings).

        :param str assistant_id: Unique identifier of the assistant. To find the
               assistant ID in the Watson Assistant user interface, open the assistant
               settings and click **API Details**. For information about creating
               assistants, see the
               [documentation](https://cloud.ibm.com/docs/services/assistant?topic=assistant-assistant-add#assistant-add-task).
               **Note:** Currently, the v2 API does not support creating assistants.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse
        """

        if assistant_id is None:
            raise ValueError('assistant_id must be provided')

        headers = {}
        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V2',
                                      operation_id='create_session')
        headers.update(sdk_headers)

        params = {'version': self.version}

        url = '/v2/assistants/{0}/sessions'.format(
            *self._encode_path_vars(assistant_id))
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response

    def delete_session(self, assistant_id: str, session_id: str,
                       **kwargs) -> 'DetailedResponse':
        """
        Delete session.

        Deletes a session explicitly before it times out. (For more information about the
        session inactivity timeout, see the
        [documentation](https://cloud.ibm.com/docs/services/assistant?topic=assistant-assistant-settings)).

        :param str assistant_id: Unique identifier of the assistant. To find the
               assistant ID in the Watson Assistant user interface, open the assistant
               settings and click **API Details**. For information about creating
               assistants, see the
               [documentation](https://cloud.ibm.com/docs/services/assistant?topic=assistant-assistant-add#assistant-add-task).
               **Note:** Currently, the v2 API does not support creating assistants.
        :param str session_id: Unique identifier of the session.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse
        """

        if assistant_id is None:
            raise ValueError('assistant_id must be provided')
        if session_id is None:
            raise ValueError('session_id must be provided')

        headers = {}
        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V2',
                                      operation_id='delete_session')
        headers.update(sdk_headers)

        params = {'version': self.version}

        url = '/v2/assistants/{0}/sessions/{1}'.format(
            *self._encode_path_vars(assistant_id, session_id))
        request = self.prepare_request(method='DELETE',
                                       url=url,
                                       headers=headers,
                                       params=params)

        response = self.send(request)
        return response

    #########################
    # Message
    #########################

    def message(self,
                assistant_id: str,
                session_id: str,
                *,
                input: 'MessageInput' = None,
                context: 'MessageContext' = None,
                **kwargs) -> 'DetailedResponse':
        """
        Send user input to assistant.

        Send user input to an assistant and receive a response.
        There is no rate limit for this operation.

        :param str assistant_id: Unique identifier of the assistant. To find the
               assistant ID in the Watson Assistant user interface, open the assistant
               settings and click **API Details**. For information about creating
               assistants, see the
               [documentation](https://cloud.ibm.com/docs/services/assistant?topic=assistant-assistant-add#assistant-add-task).
               **Note:** Currently, the v2 API does not support creating assistants.
        :param str session_id: Unique identifier of the session.
        :param MessageInput input: (optional) An input object that includes the
               input text.
        :param MessageContext context: (optional) State information for the
               conversation. The context is stored by the assistant on a per-session
               basis. You can use this property to set or modify context variables, which
               can also be accessed by dialog nodes.
        :param dict headers: A `dict` containing the request headers
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse
        """

        if assistant_id is None:
            raise ValueError('assistant_id must be provided')
        if session_id is None:
            raise ValueError('session_id must be provided')
        if input is not None:
            input = self._convert_model(input)
        if context is not None:
            context = self._convert_model(context)

        headers = {}
        if 'headers' in kwargs:
            headers.update(kwargs.get('headers'))
        sdk_headers = get_sdk_headers(service_name=self.DEFAULT_SERVICE_NAME,
                                      service_version='V2',
                                      operation_id='message')
        headers.update(sdk_headers)

        params = {'version': self.version}

        data = {'input': input, 'context': context}

        url = '/v2/assistants/{0}/sessions/{1}/message'.format(
            *self._encode_path_vars(assistant_id, session_id))
        request = self.prepare_request(method='POST',
                                       url=url,
                                       headers=headers,
                                       params=params,
                                       data=data)

        response = self.send(request)
        return response


##############################################################################
# Models
##############################################################################


class CaptureGroup():
    """
    CaptureGroup.

    :attr str group: A recognized capture group for the entity.
    :attr List[int] location: (optional) Zero-based character offsets that indicate
          where the entity value begins and ends in the input text.
    """

    def __init__(self, group: str, *, location: List[int] = None) -> None:
        """
        Initialize a CaptureGroup object.

        :param str group: A recognized capture group for the entity.
        :param List[int] location: (optional) Zero-based character offsets that
               indicate where the entity value begins and ends in the input text.
        """
        self.group = group
        self.location = location

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'CaptureGroup':
        """Initialize a CaptureGroup object from a json dictionary."""
        args = {}
        valid_keys = ['group', 'location']
        bad_keys = set(_dict.keys()) - set(valid_keys)
        if bad_keys:
            raise ValueError(
                'Unrecognized keys detected in dictionary for class CaptureGroup: '
                + ', '.join(bad_keys))
        if 'group' in _dict:
            args['group'] = _dict.get('group')
        else:
            raise ValueError(
                'Required property \'group\' not present in CaptureGroup JSON')
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a CaptureGroup object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'group') and self.group is not None:
            _dict['group'] = self.group
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this CaptureGroup object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'CaptureGroup') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'CaptureGroup') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class DialogLogMessage():
    """
    Dialog log message details.

    :attr str level: The severity of the log message.
    :attr str message: The text of the log message.
    """

    def __init__(self, level: str, message: str) -> None:
        """
        Initialize a DialogLogMessage object.

        :param str level: The severity of the log message.
        :param str message: The text of the log message.
        """
        self.level = level
        self.message = message

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'DialogLogMessage':
        """Initialize a DialogLogMessage object from a json dictionary."""
        args = {}
        valid_keys = ['level', 'message']
        bad_keys = set(_dict.keys()) - set(valid_keys)
        if bad_keys:
            raise ValueError(
                'Unrecognized keys detected in dictionary for class DialogLogMessage: '
                + ', '.join(bad_keys))
        if 'level' in _dict:
            args['level'] = _dict.get('level')
        else:
            raise ValueError(
                'Required property \'level\' not present in DialogLogMessage JSON'
            )
        if 'message' in _dict:
            args['message'] = _dict.get('message')
        else:
            raise ValueError(
                'Required property \'message\' not present in DialogLogMessage JSON'
            )
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a DialogLogMessage object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'level') and self.level is not None:
            _dict['level'] = self.level
        if hasattr(self, 'message') and self.message is not None:
            _dict['message'] = self.message
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this DialogLogMessage object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'DialogLogMessage') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'DialogLogMessage') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class LevelEnum(Enum):
        """
        The severity of the log message.
        """
        INFO = "info"
        ERROR = "error"
        WARN = "warn"


class DialogNodeAction():
    """
    DialogNodeAction.

    :attr str name: The name of the action.
    :attr str type: (optional) The type of action to invoke.
    :attr dict parameters: (optional) A map of key/value pairs to be provided to the
          action.
    :attr str result_variable: The location in the dialog context where the result
          of the action is stored.
    :attr str credentials: (optional) The name of the context variable that the
          client application will use to pass in credentials for the action.
    """

    def __init__(self,
                 name: str,
                 result_variable: str,
                 *,
                 type: str = None,
                 parameters: dict = None,
                 credentials: str = None) -> None:
        """
        Initialize a DialogNodeAction object.

        :param str name: The name of the action.
        :param str result_variable: The location in the dialog context where the
               result of the action is stored.
        :param str type: (optional) The type of action to invoke.
        :param dict parameters: (optional) A map of key/value pairs to be provided
               to the action.
        :param str credentials: (optional) The name of the context variable that
               the client application will use to pass in credentials for the action.
        """
        self.name = name
        self.type = type
        self.parameters = parameters
        self.result_variable = result_variable
        self.credentials = credentials

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'DialogNodeAction':
        """Initialize a DialogNodeAction object from a json dictionary."""
        args = {}
        valid_keys = [
            'name', 'type', 'parameters', 'result_variable', 'credentials'
        ]
        bad_keys = set(_dict.keys()) - set(valid_keys)
        if bad_keys:
            raise ValueError(
                'Unrecognized keys detected in dictionary for class DialogNodeAction: '
                + ', '.join(bad_keys))
        if 'name' in _dict:
            args['name'] = _dict.get('name')
        else:
            raise ValueError(
                'Required property \'name\' not present in DialogNodeAction JSON'
            )
        if 'type' in _dict:
            args['type'] = _dict.get('type')
        if 'parameters' in _dict:
            args['parameters'] = _dict.get('parameters')
        if 'result_variable' in _dict:
            args['result_variable'] = _dict.get('result_variable')
        else:
            raise ValueError(
                'Required property \'result_variable\' not present in DialogNodeAction JSON'
            )
        if 'credentials' in _dict:
            args['credentials'] = _dict.get('credentials')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a DialogNodeAction object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'name') and self.name is not None:
            _dict['name'] = self.name
        if hasattr(self, 'type') and self.type is not None:
            _dict['type'] = self.type
        if hasattr(self, 'parameters') and self.parameters is not None:
            _dict['parameters'] = self.parameters
        if hasattr(self,
                   'result_variable') and self.result_variable is not None:
            _dict['result_variable'] = self.result_variable
        if hasattr(self, 'credentials') and self.credentials is not None:
            _dict['credentials'] = self.credentials
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this DialogNodeAction object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'DialogNodeAction') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'DialogNodeAction') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class TypeEnum(Enum):
        """
        The type of action to invoke.
        """
        CLIENT = "client"
        SERVER = "server"
        WEB_ACTION = "web-action"
        CLOUD_FUNCTION = "cloud-function"


class DialogNodeOutputOptionsElement():
    """
    DialogNodeOutputOptionsElement.

    :attr str label: The user-facing label for the option.
    :attr DialogNodeOutputOptionsElementValue value: An object defining the message
          input to be sent to the assistant if the user selects the corresponding option.
    """

    def __init__(self, label: str,
                 value: 'DialogNodeOutputOptionsElementValue') -> None:
        """
        Initialize a DialogNodeOutputOptionsElement object.

        :param str label: The user-facing label for the option.
        :param DialogNodeOutputOptionsElementValue value: An object defining the
               message input to be sent to the assistant if the user selects the
               corresponding option.
        """
        self.label = label
        self.value = value

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'DialogNodeOutputOptionsElement':
        """Initialize a DialogNodeOutputOptionsElement object from a json dictionary."""
        args = {}
        valid_keys = ['label', 'value']
        bad_keys = set(_dict.keys()) - set(valid_keys)
        if bad_keys:
            raise ValueError(
                'Unrecognized keys detected in dictionary for class DialogNodeOutputOptionsElement: '
                + ', '.join(bad_keys))
        if 'label' in _dict:
            args['label'] = _dict.get('label')
        else:
            raise ValueError(
                'Required property \'label\' not present in DialogNodeOutputOptionsElement JSON'
            )
        if 'value' in _dict:
            args['value'] = DialogNodeOutputOptionsElementValue._from_dict(
                _dict.get('value'))
        else:
            raise ValueError(
                'Required property \'value\' not present in DialogNodeOutputOptionsElement JSON'
            )
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a DialogNodeOutputOptionsElement object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'label') and self.label is not None:
            _dict['label'] = self.label
        if hasattr(self, 'value') and self.value is not None:
            _dict['value'] = self.value._to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this DialogNodeOutputOptionsElement object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'DialogNodeOutputOptionsElement') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'DialogNodeOutputOptionsElement') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class DialogNodeOutputOptionsElementValue():
    """
    An object defining the message input to be sent to the assistant if the user selects
    the corresponding option.

    :attr MessageInput input: (optional) An input object that includes the input
          text.
    """

    def __init__(self, *, input: 'MessageInput' = None) -> None:
        """
        Initialize a DialogNodeOutputOptionsElementValue object.

        :param MessageInput input: (optional) An input object that includes the
               input text.
        """
        self.input = input

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'DialogNodeOutputOptionsElementValue':
        """Initialize a DialogNodeOutputOptionsElementValue object from a json dictionary."""
        args = {}
        valid_keys = ['input']
        bad_keys = set(_dict.keys()) - set(valid_keys)
        if bad_keys:
            raise ValueError(
                'Unrecognized keys detected in dictionary for class DialogNodeOutputOptionsElementValue: '
                + ', '.join(bad_keys))
        if 'input' in _dict:
            args['input'] = MessageInput._from_dict(_dict.get('input'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a DialogNodeOutputOptionsElementValue object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'input') and self.input is not None:
            _dict['input'] = self.input._to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this DialogNodeOutputOptionsElementValue object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'DialogNodeOutputOptionsElementValue') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'DialogNodeOutputOptionsElementValue') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class DialogNodesVisited():
    """
    DialogNodesVisited.

    :attr str dialog_node: (optional) A dialog node that was triggered during
          processing of the input message.
    :attr str title: (optional) The title of the dialog node.
    :attr str conditions: (optional) The conditions that trigger the dialog node.
    """

    def __init__(self,
                 *,
                 dialog_node: str = None,
                 title: str = None,
                 conditions: str = None) -> None:
        """
        Initialize a DialogNodesVisited object.

        :param str dialog_node: (optional) A dialog node that was triggered during
               processing of the input message.
        :param str title: (optional) The title of the dialog node.
        :param str conditions: (optional) The conditions that trigger the dialog
               node.
        """
        self.dialog_node = dialog_node
        self.title = title
        self.conditions = conditions

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'DialogNodesVisited':
        """Initialize a DialogNodesVisited object from a json dictionary."""
        args = {}
        valid_keys = ['dialog_node', 'title', 'conditions']
        bad_keys = set(_dict.keys()) - set(valid_keys)
        if bad_keys:
            raise ValueError(
                'Unrecognized keys detected in dictionary for class DialogNodesVisited: '
                + ', '.join(bad_keys))
        if 'dialog_node' in _dict:
            args['dialog_node'] = _dict.get('dialog_node')
        if 'title' in _dict:
            args['title'] = _dict.get('title')
        if 'conditions' in _dict:
            args['conditions'] = _dict.get('conditions')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a DialogNodesVisited object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'dialog_node') and self.dialog_node is not None:
            _dict['dialog_node'] = self.dialog_node
        if hasattr(self, 'title') and self.title is not None:
            _dict['title'] = self.title
        if hasattr(self, 'conditions') and self.conditions is not None:
            _dict['conditions'] = self.conditions
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this DialogNodesVisited object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'DialogNodesVisited') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'DialogNodesVisited') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class DialogSuggestion():
    """
    DialogSuggestion.

    :attr str label: The user-facing label for the disambiguation option. This label
          is taken from the **title** or **user_label** property of the corresponding
          dialog node, depending on the disambiguation options.
    :attr DialogSuggestionValue value: An object defining the message input to be
          sent to the assistant if the user selects the corresponding disambiguation
          option.
    :attr dict output: (optional) The dialog output that will be returned from the
          Watson Assistant service if the user selects the corresponding option.
    """

    def __init__(self,
                 label: str,
                 value: 'DialogSuggestionValue',
                 *,
                 output: dict = None) -> None:
        """
        Initialize a DialogSuggestion object.

        :param str label: The user-facing label for the disambiguation option. This
               label is taken from the **title** or **user_label** property of the
               corresponding dialog node, depending on the disambiguation options.
        :param DialogSuggestionValue value: An object defining the message input to
               be sent to the assistant if the user selects the corresponding
               disambiguation option.
        :param dict output: (optional) The dialog output that will be returned from
               the Watson Assistant service if the user selects the corresponding option.
        """
        self.label = label
        self.value = value
        self.output = output

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'DialogSuggestion':
        """Initialize a DialogSuggestion object from a json dictionary."""
        args = {}
        valid_keys = ['label', 'value', 'output']
        bad_keys = set(_dict.keys()) - set(valid_keys)
        if bad_keys:
            raise ValueError(
                'Unrecognized keys detected in dictionary for class DialogSuggestion: '
                + ', '.join(bad_keys))
        if 'label' in _dict:
            args['label'] = _dict.get('label')
        else:
            raise ValueError(
                'Required property \'label\' not present in DialogSuggestion JSON'
            )
        if 'value' in _dict:
            args['value'] = DialogSuggestionValue._from_dict(_dict.get('value'))
        else:
            raise ValueError(
                'Required property \'value\' not present in DialogSuggestion JSON'
            )
        if 'output' in _dict:
            args['output'] = _dict.get('output')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a DialogSuggestion object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'label') and self.label is not None:
            _dict['label'] = self.label
        if hasattr(self, 'value') and self.value is not None:
            _dict['value'] = self.value._to_dict()
        if hasattr(self, 'output') and self.output is not None:
            _dict['output'] = self.output
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this DialogSuggestion object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'DialogSuggestion') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'DialogSuggestion') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class DialogSuggestionValue():
    """
    An object defining the message input to be sent to the assistant if the user selects
    the corresponding disambiguation option.

    :attr MessageInput input: (optional) An input object that includes the input
          text.
    """

    def __init__(self, *, input: 'MessageInput' = None) -> None:
        """
        Initialize a DialogSuggestionValue object.

        :param MessageInput input: (optional) An input object that includes the
               input text.
        """
        self.input = input

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'DialogSuggestionValue':
        """Initialize a DialogSuggestionValue object from a json dictionary."""
        args = {}
        valid_keys = ['input']
        bad_keys = set(_dict.keys()) - set(valid_keys)
        if bad_keys:
            raise ValueError(
                'Unrecognized keys detected in dictionary for class DialogSuggestionValue: '
                + ', '.join(bad_keys))
        if 'input' in _dict:
            args['input'] = MessageInput._from_dict(_dict.get('input'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a DialogSuggestionValue object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'input') and self.input is not None:
            _dict['input'] = self.input._to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this DialogSuggestionValue object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'DialogSuggestionValue') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'DialogSuggestionValue') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class MessageContext():
    """
    MessageContext.

    :attr MessageContextGlobal global_: (optional) Information that is shared by all
          skills used by the Assistant.
    :attr MessageContextSkills skills: (optional) Information specific to particular
          skills used by the Assistant.
          **Note:** Currently, only a single property named `main skill` is supported.
          This object contains variables that apply to the dialog skill used by the
          assistant.
    """

    def __init__(self,
                 *,
                 global_: 'MessageContextGlobal' = None,
                 skills: 'MessageContextSkills' = None) -> None:
        """
        Initialize a MessageContext object.

        :param MessageContextGlobal global_: (optional) Information that is shared
               by all skills used by the Assistant.
        :param MessageContextSkills skills: (optional) Information specific to
               particular skills used by the Assistant.
               **Note:** Currently, only a single property named `main skill` is
               supported. This object contains variables that apply to the dialog skill
               used by the assistant.
        """
        self.global_ = global_
        self.skills = skills

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'MessageContext':
        """Initialize a MessageContext object from a json dictionary."""
        args = {}
        valid_keys = ['global_', 'global', 'skills']
        bad_keys = set(_dict.keys()) - set(valid_keys)
        if bad_keys:
            raise ValueError(
                'Unrecognized keys detected in dictionary for class MessageContext: '
                + ', '.join(bad_keys))
        if 'global' in _dict:
            args['global_'] = MessageContextGlobal._from_dict(
                _dict.get('global'))
        if 'skills' in _dict:
            args['skills'] = MessageContextSkills._from_dict(
                _dict.get('skills'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a MessageContext object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'global_') and self.global_ is not None:
            _dict['global'] = self.global_._to_dict()
        if hasattr(self, 'skills') and self.skills is not None:
            _dict['skills'] = self.skills._to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this MessageContext object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'MessageContext') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'MessageContext') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class MessageContextGlobal():
    """
    Information that is shared by all skills used by the Assistant.

    :attr MessageContextGlobalSystem system: (optional) Built-in system properties
          that apply to all skills used by the assistant.
    """

    def __init__(self, *, system: 'MessageContextGlobalSystem' = None) -> None:
        """
        Initialize a MessageContextGlobal object.

        :param MessageContextGlobalSystem system: (optional) Built-in system
               properties that apply to all skills used by the assistant.
        """
        self.system = system

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'MessageContextGlobal':
        """Initialize a MessageContextGlobal object from a json dictionary."""
        args = {}
        valid_keys = ['system']
        bad_keys = set(_dict.keys()) - set(valid_keys)
        if bad_keys:
            raise ValueError(
                'Unrecognized keys detected in dictionary for class MessageContextGlobal: '
                + ', '.join(bad_keys))
        if 'system' in _dict:
            args['system'] = MessageContextGlobalSystem._from_dict(
                _dict.get('system'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a MessageContextGlobal object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'system') and self.system is not None:
            _dict['system'] = self.system._to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this MessageContextGlobal object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'MessageContextGlobal') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'MessageContextGlobal') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class MessageContextGlobalSystem():
    """
    Built-in system properties that apply to all skills used by the assistant.

    :attr str timezone: (optional) The user time zone. The assistant uses the time
          zone to correctly resolve relative time references.
    :attr str user_id: (optional) A string value that identifies the user who is
          interacting with the assistant. The client must provide a unique identifier for
          each individual end user who accesses the application. For Plus and Premium
          plans, this user ID is used to identify unique users for billing purposes. This
          string cannot contain carriage return, newline, or tab characters.
    :attr int turn_count: (optional) A counter that is automatically incremented
          with each turn of the conversation. A value of 1 indicates that this is the the
          first turn of a new conversation, which can affect the behavior of some skills
          (for example, triggering the start node of a dialog).
    """

    def __init__(self,
                 *,
                 timezone: str = None,
                 user_id: str = None,
                 turn_count: int = None) -> None:
        """
        Initialize a MessageContextGlobalSystem object.

        :param str timezone: (optional) The user time zone. The assistant uses the
               time zone to correctly resolve relative time references.
        :param str user_id: (optional) A string value that identifies the user who
               is interacting with the assistant. The client must provide a unique
               identifier for each individual end user who accesses the application. For
               Plus and Premium plans, this user ID is used to identify unique users for
               billing purposes. This string cannot contain carriage return, newline, or
               tab characters.
        :param int turn_count: (optional) A counter that is automatically
               incremented with each turn of the conversation. A value of 1 indicates that
               this is the the first turn of a new conversation, which can affect the
               behavior of some skills (for example, triggering the start node of a
               dialog).
        """
        self.timezone = timezone
        self.user_id = user_id
        self.turn_count = turn_count

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'MessageContextGlobalSystem':
        """Initialize a MessageContextGlobalSystem object from a json dictionary."""
        args = {}
        valid_keys = ['timezone', 'user_id', 'turn_count']
        bad_keys = set(_dict.keys()) - set(valid_keys)
        if bad_keys:
            raise ValueError(
                'Unrecognized keys detected in dictionary for class MessageContextGlobalSystem: '
                + ', '.join(bad_keys))
        if 'timezone' in _dict:
            args['timezone'] = _dict.get('timezone')
        if 'user_id' in _dict:
            args['user_id'] = _dict.get('user_id')
        if 'turn_count' in _dict:
            args['turn_count'] = _dict.get('turn_count')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a MessageContextGlobalSystem object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'timezone') and self.timezone is not None:
            _dict['timezone'] = self.timezone
        if hasattr(self, 'user_id') and self.user_id is not None:
            _dict['user_id'] = self.user_id
        if hasattr(self, 'turn_count') and self.turn_count is not None:
            _dict['turn_count'] = self.turn_count
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this MessageContextGlobalSystem object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'MessageContextGlobalSystem') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'MessageContextGlobalSystem') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class MessageContextSkill():
    """
    Contains information specific to a particular skill used by the Assistant.

    :attr dict user_defined: (optional) Arbitrary variables that can be read and
          written by a particular skill.
    :attr dict system: (optional) For internal use only.
    """

    def __init__(self, *, user_defined: dict = None,
                 system: dict = None) -> None:
        """
        Initialize a MessageContextSkill object.

        :param dict user_defined: (optional) Arbitrary variables that can be read
               and written by a particular skill.
        :param dict system: (optional) For internal use only.
        """
        self.user_defined = user_defined
        self.system = system

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'MessageContextSkill':
        """Initialize a MessageContextSkill object from a json dictionary."""
        args = {}
        valid_keys = ['user_defined', 'system']
        bad_keys = set(_dict.keys()) - set(valid_keys)
        if bad_keys:
            raise ValueError(
                'Unrecognized keys detected in dictionary for class MessageContextSkill: '
                + ', '.join(bad_keys))
        if 'user_defined' in _dict:
            args['user_defined'] = _dict.get('user_defined')
        if 'system' in _dict:
            args['system'] = _dict.get('system')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a MessageContextSkill object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'user_defined') and self.user_defined is not None:
            _dict['user_defined'] = self.user_defined
        if hasattr(self, 'system') and self.system is not None:
            _dict['system'] = self.system
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this MessageContextSkill object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'MessageContextSkill') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'MessageContextSkill') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class MessageContextSkills():
    """
    Information specific to particular skills used by the Assistant.
    **Note:** Currently, only a single property named `main skill` is supported. This
    object contains variables that apply to the dialog skill used by the assistant.

    """

    def __init__(self, **kwargs) -> None:
        """
        Initialize a MessageContextSkills object.

        :param **kwargs: (optional) Any additional properties.
        """
        for _key, _value in kwargs.items():
            setattr(self, _key, _value)

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'MessageContextSkills':
        """Initialize a MessageContextSkills object from a json dictionary."""
        args = {}
        xtra = _dict.copy()
        args.update(xtra)
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a MessageContextSkills object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, '_additionalProperties'):
            for _key in self._additionalProperties:
                _value = getattr(self, _key, None)
                if _value is not None:
                    _dict[_key] = _value
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __setattr__(self, name: str, value: object) -> None:
        properties = {}
        if not hasattr(self, '_additionalProperties'):
            super(MessageContextSkills,
                  self).__setattr__('_additionalProperties', set())
        if name not in properties:
            self._additionalProperties.add(name)
        super(MessageContextSkills, self).__setattr__(name, value)

    def __str__(self) -> str:
        """Return a `str` version of this MessageContextSkills object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'MessageContextSkills') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'MessageContextSkills') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class MessageInput():
    """
    An input object that includes the input text.

    :attr str message_type: (optional) The type of user input. Currently, only text
          input is supported.
    :attr str text: (optional) The text of the user input. This string cannot
          contain carriage return, newline, or tab characters.
    :attr MessageInputOptions options: (optional) Optional properties that control
          how the assistant responds.
    :attr List[RuntimeIntent] intents: (optional) Intents to use when evaluating the
          user input. Include intents from the previous response to continue using those
          intents rather than trying to recognize intents in the new input.
    :attr List[RuntimeEntity] entities: (optional) Entities to use when evaluating
          the message. Include entities from the previous response to continue using those
          entities rather than detecting entities in the new input.
    :attr str suggestion_id: (optional) For internal use only.
    """

    def __init__(self,
                 *,
                 message_type: str = None,
                 text: str = None,
                 options: 'MessageInputOptions' = None,
                 intents: List['RuntimeIntent'] = None,
                 entities: List['RuntimeEntity'] = None,
                 suggestion_id: str = None) -> None:
        """
        Initialize a MessageInput object.

        :param str message_type: (optional) The type of user input. Currently, only
               text input is supported.
        :param str text: (optional) The text of the user input. This string cannot
               contain carriage return, newline, or tab characters.
        :param MessageInputOptions options: (optional) Optional properties that
               control how the assistant responds.
        :param List[RuntimeIntent] intents: (optional) Intents to use when
               evaluating the user input. Include intents from the previous response to
               continue using those intents rather than trying to recognize intents in the
               new input.
        :param List[RuntimeEntity] entities: (optional) Entities to use when
               evaluating the message. Include entities from the previous response to
               continue using those entities rather than detecting entities in the new
               input.
        :param str suggestion_id: (optional) For internal use only.
        """
        self.message_type = message_type
        self.text = text
        self.options = options
        self.intents = intents
        self.entities = entities
        self.suggestion_id = suggestion_id

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'MessageInput':
        """Initialize a MessageInput object from a json dictionary."""
        args = {}
        valid_keys = [
            'message_type', 'text', 'options', 'intents', 'entities',
            'suggestion_id'
        ]
        bad_keys = set(_dict.keys()) - set(valid_keys)
        if bad_keys:
            raise ValueError(
                'Unrecognized keys detected in dictionary for class MessageInput: '
                + ', '.join(bad_keys))
        if 'message_type' in _dict:
            args['message_type'] = _dict.get('message_type')
        if 'text' in _dict:
            args['text'] = _dict.get('text')
        if 'options' in _dict:
            args['options'] = MessageInputOptions._from_dict(
                _dict.get('options'))
        if 'intents' in _dict:
            args['intents'] = [
                RuntimeIntent._from_dict(x) for x in (_dict.get('intents'))
            ]
        if 'entities' in _dict:
            args['entities'] = [
                RuntimeEntity._from_dict(x) for x in (_dict.get('entities'))
            ]
        if 'suggestion_id' in _dict:
            args['suggestion_id'] = _dict.get('suggestion_id')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a MessageInput object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'message_type') and self.message_type is not None:
            _dict['message_type'] = self.message_type
        if hasattr(self, 'text') and self.text is not None:
            _dict['text'] = self.text
        if hasattr(self, 'options') and self.options is not None:
            _dict['options'] = self.options._to_dict()
        if hasattr(self, 'intents') and self.intents is not None:
            _dict['intents'] = [x._to_dict() for x in self.intents]
        if hasattr(self, 'entities') and self.entities is not None:
            _dict['entities'] = [x._to_dict() for x in self.entities]
        if hasattr(self, 'suggestion_id') and self.suggestion_id is not None:
            _dict['suggestion_id'] = self.suggestion_id
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this MessageInput object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'MessageInput') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'MessageInput') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class MessageTypeEnum(Enum):
        """
        The type of user input. Currently, only text input is supported.
        """
        TEXT = "text"


class MessageInputOptions():
    """
    Optional properties that control how the assistant responds.

    :attr bool debug: (optional) Whether to return additional diagnostic
          information. Set to `true` to return additional information under the
          `output.debug` key.
    :attr bool restart: (optional) Whether to restart dialog processing at the root
          of the dialog, regardless of any previously visited nodes. **Note:** This does
          not affect `turn_count` or any other context variables.
    :attr bool alternate_intents: (optional) Whether to return more than one intent.
          Set to `true` to return all matching intents.
    :attr bool return_context: (optional) Whether to return session context with the
          response. If you specify `true`, the response will include the `context`
          property.
    """

    def __init__(self,
                 *,
                 debug: bool = None,
                 restart: bool = None,
                 alternate_intents: bool = None,
                 return_context: bool = None) -> None:
        """
        Initialize a MessageInputOptions object.

        :param bool debug: (optional) Whether to return additional diagnostic
               information. Set to `true` to return additional information under the
               `output.debug` key.
        :param bool restart: (optional) Whether to restart dialog processing at the
               root of the dialog, regardless of any previously visited nodes. **Note:**
               This does not affect `turn_count` or any other context variables.
        :param bool alternate_intents: (optional) Whether to return more than one
               intent. Set to `true` to return all matching intents.
        :param bool return_context: (optional) Whether to return session context
               with the response. If you specify `true`, the response will include the
               `context` property.
        """
        self.debug = debug
        self.restart = restart
        self.alternate_intents = alternate_intents
        self.return_context = return_context

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'MessageInputOptions':
        """Initialize a MessageInputOptions object from a json dictionary."""
        args = {}
        valid_keys = ['debug', 'restart', 'alternate_intents', 'return_context']
        bad_keys = set(_dict.keys()) - set(valid_keys)
        if bad_keys:
            raise ValueError(
                'Unrecognized keys detected in dictionary for class MessageInputOptions: '
                + ', '.join(bad_keys))
        if 'debug' in _dict:
            args['debug'] = _dict.get('debug')
        if 'restart' in _dict:
            args['restart'] = _dict.get('restart')
        if 'alternate_intents' in _dict:
            args['alternate_intents'] = _dict.get('alternate_intents')
        if 'return_context' in _dict:
            args['return_context'] = _dict.get('return_context')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a MessageInputOptions object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'debug') and self.debug is not None:
            _dict['debug'] = self.debug
        if hasattr(self, 'restart') and self.restart is not None:
            _dict['restart'] = self.restart
        if hasattr(self,
                   'alternate_intents') and self.alternate_intents is not None:
            _dict['alternate_intents'] = self.alternate_intents
        if hasattr(self, 'return_context') and self.return_context is not None:
            _dict['return_context'] = self.return_context
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this MessageInputOptions object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'MessageInputOptions') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'MessageInputOptions') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class MessageOutput():
    """
    Assistant output to be rendered or processed by the client.

    :attr List[RuntimeResponseGeneric] generic: (optional) Output intended for any
          channel. It is the responsibility of the client application to implement the
          supported response types.
    :attr List[RuntimeIntent] intents: (optional) An array of intents recognized in
          the user input, sorted in descending order of confidence.
    :attr List[RuntimeEntity] entities: (optional) An array of entities identified
          in the user input.
    :attr List[DialogNodeAction] actions: (optional) An array of objects describing
          any actions requested by the dialog node.
    :attr MessageOutputDebug debug: (optional) Additional detailed information about
          a message response and how it was generated.
    :attr dict user_defined: (optional) An object containing any custom properties
          included in the response. This object includes any arbitrary properties defined
          in the dialog JSON editor as part of the dialog node output.
    """

    def __init__(self,
                 *,
                 generic: List['RuntimeResponseGeneric'] = None,
                 intents: List['RuntimeIntent'] = None,
                 entities: List['RuntimeEntity'] = None,
                 actions: List['DialogNodeAction'] = None,
                 debug: 'MessageOutputDebug' = None,
                 user_defined: dict = None) -> None:
        """
        Initialize a MessageOutput object.

        :param List[RuntimeResponseGeneric] generic: (optional) Output intended for
               any channel. It is the responsibility of the client application to
               implement the supported response types.
        :param List[RuntimeIntent] intents: (optional) An array of intents
               recognized in the user input, sorted in descending order of confidence.
        :param List[RuntimeEntity] entities: (optional) An array of entities
               identified in the user input.
        :param List[DialogNodeAction] actions: (optional) An array of objects
               describing any actions requested by the dialog node.
        :param MessageOutputDebug debug: (optional) Additional detailed information
               about a message response and how it was generated.
        :param dict user_defined: (optional) An object containing any custom
               properties included in the response. This object includes any arbitrary
               properties defined in the dialog JSON editor as part of the dialog node
               output.
        """
        self.generic = generic
        self.intents = intents
        self.entities = entities
        self.actions = actions
        self.debug = debug
        self.user_defined = user_defined

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'MessageOutput':
        """Initialize a MessageOutput object from a json dictionary."""
        args = {}
        valid_keys = [
            'generic', 'intents', 'entities', 'actions', 'debug', 'user_defined'
        ]
        bad_keys = set(_dict.keys()) - set(valid_keys)
        if bad_keys:
            raise ValueError(
                'Unrecognized keys detected in dictionary for class MessageOutput: '
                + ', '.join(bad_keys))
        if 'generic' in _dict:
            args['generic'] = [
                RuntimeResponseGeneric._from_dict(x)
                for x in (_dict.get('generic'))
            ]
        if 'intents' in _dict:
            args['intents'] = [
                RuntimeIntent._from_dict(x) for x in (_dict.get('intents'))
            ]
        if 'entities' in _dict:
            args['entities'] = [
                RuntimeEntity._from_dict(x) for x in (_dict.get('entities'))
            ]
        if 'actions' in _dict:
            args['actions'] = [
                DialogNodeAction._from_dict(x) for x in (_dict.get('actions'))
            ]
        if 'debug' in _dict:
            args['debug'] = MessageOutputDebug._from_dict(_dict.get('debug'))
        if 'user_defined' in _dict:
            args['user_defined'] = _dict.get('user_defined')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a MessageOutput object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'generic') and self.generic is not None:
            _dict['generic'] = [x._to_dict() for x in self.generic]
        if hasattr(self, 'intents') and self.intents is not None:
            _dict['intents'] = [x._to_dict() for x in self.intents]
        if hasattr(self, 'entities') and self.entities is not None:
            _dict['entities'] = [x._to_dict() for x in self.entities]
        if hasattr(self, 'actions') and self.actions is not None:
            _dict['actions'] = [x._to_dict() for x in self.actions]
        if hasattr(self, 'debug') and self.debug is not None:
            _dict['debug'] = self.debug._to_dict()
        if hasattr(self, 'user_defined') and self.user_defined is not None:
            _dict['user_defined'] = self.user_defined
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this MessageOutput object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'MessageOutput') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'MessageOutput') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class MessageOutputDebug():
    """
    Additional detailed information about a message response and how it was generated.

    :attr List[DialogNodesVisited] nodes_visited: (optional) An array of objects
          containing detailed diagnostic information about the nodes that were triggered
          during processing of the input message.
    :attr List[DialogLogMessage] log_messages: (optional) An array of up to 50
          messages logged with the request.
    :attr bool branch_exited: (optional) Assistant sets this to true when this
          message response concludes or interrupts a dialog.
    :attr str branch_exited_reason: (optional) When `branch_exited` is set to `true`
          by the Assistant, the `branch_exited_reason` specifies whether the dialog
          completed by itself or got interrupted.
    """

    def __init__(self,
                 *,
                 nodes_visited: List['DialogNodesVisited'] = None,
                 log_messages: List['DialogLogMessage'] = None,
                 branch_exited: bool = None,
                 branch_exited_reason: str = None) -> None:
        """
        Initialize a MessageOutputDebug object.

        :param List[DialogNodesVisited] nodes_visited: (optional) An array of
               objects containing detailed diagnostic information about the nodes that
               were triggered during processing of the input message.
        :param List[DialogLogMessage] log_messages: (optional) An array of up to 50
               messages logged with the request.
        :param bool branch_exited: (optional) Assistant sets this to true when this
               message response concludes or interrupts a dialog.
        :param str branch_exited_reason: (optional) When `branch_exited` is set to
               `true` by the Assistant, the `branch_exited_reason` specifies whether the
               dialog completed by itself or got interrupted.
        """
        self.nodes_visited = nodes_visited
        self.log_messages = log_messages
        self.branch_exited = branch_exited
        self.branch_exited_reason = branch_exited_reason

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'MessageOutputDebug':
        """Initialize a MessageOutputDebug object from a json dictionary."""
        args = {}
        valid_keys = [
            'nodes_visited', 'log_messages', 'branch_exited',
            'branch_exited_reason'
        ]
        bad_keys = set(_dict.keys()) - set(valid_keys)
        if bad_keys:
            raise ValueError(
                'Unrecognized keys detected in dictionary for class MessageOutputDebug: '
                + ', '.join(bad_keys))
        if 'nodes_visited' in _dict:
            args['nodes_visited'] = [
                DialogNodesVisited._from_dict(x)
                for x in (_dict.get('nodes_visited'))
            ]
        if 'log_messages' in _dict:
            args['log_messages'] = [
                DialogLogMessage._from_dict(x)
                for x in (_dict.get('log_messages'))
            ]
        if 'branch_exited' in _dict:
            args['branch_exited'] = _dict.get('branch_exited')
        if 'branch_exited_reason' in _dict:
            args['branch_exited_reason'] = _dict.get('branch_exited_reason')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a MessageOutputDebug object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'nodes_visited') and self.nodes_visited is not None:
            _dict['nodes_visited'] = [x._to_dict() for x in self.nodes_visited]
        if hasattr(self, 'log_messages') and self.log_messages is not None:
            _dict['log_messages'] = [x._to_dict() for x in self.log_messages]
        if hasattr(self, 'branch_exited') and self.branch_exited is not None:
            _dict['branch_exited'] = self.branch_exited
        if hasattr(self, 'branch_exited_reason'
                  ) and self.branch_exited_reason is not None:
            _dict['branch_exited_reason'] = self.branch_exited_reason
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this MessageOutputDebug object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'MessageOutputDebug') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'MessageOutputDebug') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class BranchExitedReasonEnum(Enum):
        """
        When `branch_exited` is set to `true` by the Assistant, the `branch_exited_reason`
        specifies whether the dialog completed by itself or got interrupted.
        """
        COMPLETED = "completed"
        FALLBACK = "fallback"


class MessageResponse():
    """
    A response from the Watson Assistant service.

    :attr MessageOutput output: Assistant output to be rendered or processed by the
          client.
    :attr MessageContext context: (optional) State information for the conversation.
          The context is stored by the assistant on a per-session basis. You can use this
          property to access context variables.
          **Note:** The context is included in message responses only if
          **return_context**=`true` in the message request.
    """

    def __init__(self,
                 output: 'MessageOutput',
                 *,
                 context: 'MessageContext' = None) -> None:
        """
        Initialize a MessageResponse object.

        :param MessageOutput output: Assistant output to be rendered or processed
               by the client.
        :param MessageContext context: (optional) State information for the
               conversation. The context is stored by the assistant on a per-session
               basis. You can use this property to access context variables.
               **Note:** The context is included in message responses only if
               **return_context**=`true` in the message request.
        """
        self.output = output
        self.context = context

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'MessageResponse':
        """Initialize a MessageResponse object from a json dictionary."""
        args = {}
        valid_keys = ['output', 'context']
        bad_keys = set(_dict.keys()) - set(valid_keys)
        if bad_keys:
            raise ValueError(
                'Unrecognized keys detected in dictionary for class MessageResponse: '
                + ', '.join(bad_keys))
        if 'output' in _dict:
            args['output'] = MessageOutput._from_dict(_dict.get('output'))
        else:
            raise ValueError(
                'Required property \'output\' not present in MessageResponse JSON'
            )
        if 'context' in _dict:
            args['context'] = MessageContext._from_dict(_dict.get('context'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a MessageResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'output') and self.output is not None:
            _dict['output'] = self.output._to_dict()
        if hasattr(self, 'context') and self.context is not None:
            _dict['context'] = self.context._to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this MessageResponse object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'MessageResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'MessageResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class RuntimeEntity():
    """
    The entity value that was recognized in the user input.

    :attr str entity: An entity detected in the input.
    :attr List[int] location: An array of zero-based character offsets that indicate
          where the detected entity values begin and end in the input text.
    :attr str value: The term in the input text that was recognized as an entity
          value.
    :attr float confidence: (optional) A decimal percentage that represents Watson's
          confidence in the recognized entity.
    :attr dict metadata: (optional) Any metadata for the entity.
    :attr List[CaptureGroup] groups: (optional) The recognized capture groups for
          the entity, as defined by the entity pattern.
    """

    def __init__(self,
                 entity: str,
                 location: List[int],
                 value: str,
                 *,
                 confidence: float = None,
                 metadata: dict = None,
                 groups: List['CaptureGroup'] = None) -> None:
        """
        Initialize a RuntimeEntity object.

        :param str entity: An entity detected in the input.
        :param List[int] location: An array of zero-based character offsets that
               indicate where the detected entity values begin and end in the input text.
        :param str value: The term in the input text that was recognized as an
               entity value.
        :param float confidence: (optional) A decimal percentage that represents
               Watson's confidence in the recognized entity.
        :param dict metadata: (optional) Any metadata for the entity.
        :param List[CaptureGroup] groups: (optional) The recognized capture groups
               for the entity, as defined by the entity pattern.
        """
        self.entity = entity
        self.location = location
        self.value = value
        self.confidence = confidence
        self.metadata = metadata
        self.groups = groups

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'RuntimeEntity':
        """Initialize a RuntimeEntity object from a json dictionary."""
        args = {}
        valid_keys = [
            'entity', 'location', 'value', 'confidence', 'metadata', 'groups'
        ]
        bad_keys = set(_dict.keys()) - set(valid_keys)
        if bad_keys:
            raise ValueError(
                'Unrecognized keys detected in dictionary for class RuntimeEntity: '
                + ', '.join(bad_keys))
        if 'entity' in _dict:
            args['entity'] = _dict.get('entity')
        else:
            raise ValueError(
                'Required property \'entity\' not present in RuntimeEntity JSON'
            )
        if 'location' in _dict:
            args['location'] = _dict.get('location')
        else:
            raise ValueError(
                'Required property \'location\' not present in RuntimeEntity JSON'
            )
        if 'value' in _dict:
            args['value'] = _dict.get('value')
        else:
            raise ValueError(
                'Required property \'value\' not present in RuntimeEntity JSON')
        if 'confidence' in _dict:
            args['confidence'] = _dict.get('confidence')
        if 'metadata' in _dict:
            args['metadata'] = _dict.get('metadata')
        if 'groups' in _dict:
            args['groups'] = [
                CaptureGroup._from_dict(x) for x in (_dict.get('groups'))
            ]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a RuntimeEntity object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'entity') and self.entity is not None:
            _dict['entity'] = self.entity
        if hasattr(self, 'location') and self.location is not None:
            _dict['location'] = self.location
        if hasattr(self, 'value') and self.value is not None:
            _dict['value'] = self.value
        if hasattr(self, 'confidence') and self.confidence is not None:
            _dict['confidence'] = self.confidence
        if hasattr(self, 'metadata') and self.metadata is not None:
            _dict['metadata'] = self.metadata
        if hasattr(self, 'groups') and self.groups is not None:
            _dict['groups'] = [x._to_dict() for x in self.groups]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this RuntimeEntity object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'RuntimeEntity') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'RuntimeEntity') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class RuntimeIntent():
    """
    An intent identified in the user input.

    :attr str intent: The name of the recognized intent.
    :attr float confidence: A decimal percentage that represents Watson's confidence
          in the intent.
    """

    def __init__(self, intent: str, confidence: float) -> None:
        """
        Initialize a RuntimeIntent object.

        :param str intent: The name of the recognized intent.
        :param float confidence: A decimal percentage that represents Watson's
               confidence in the intent.
        """
        self.intent = intent
        self.confidence = confidence

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'RuntimeIntent':
        """Initialize a RuntimeIntent object from a json dictionary."""
        args = {}
        valid_keys = ['intent', 'confidence']
        bad_keys = set(_dict.keys()) - set(valid_keys)
        if bad_keys:
            raise ValueError(
                'Unrecognized keys detected in dictionary for class RuntimeIntent: '
                + ', '.join(bad_keys))
        if 'intent' in _dict:
            args['intent'] = _dict.get('intent')
        else:
            raise ValueError(
                'Required property \'intent\' not present in RuntimeIntent JSON'
            )
        if 'confidence' in _dict:
            args['confidence'] = _dict.get('confidence')
        else:
            raise ValueError(
                'Required property \'confidence\' not present in RuntimeIntent JSON'
            )
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a RuntimeIntent object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'intent') and self.intent is not None:
            _dict['intent'] = self.intent
        if hasattr(self, 'confidence') and self.confidence is not None:
            _dict['confidence'] = self.confidence
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this RuntimeIntent object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'RuntimeIntent') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'RuntimeIntent') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class RuntimeResponseGeneric():
    """
    RuntimeResponseGeneric.

    :attr str response_type: The type of response returned by the dialog node. The
          specified response type must be supported by the client application or channel.
          **Note:** The **suggestion** response type is part of the disambiguation
          feature, which is only available for Premium users.
    :attr str text: (optional) The text of the response.
    :attr int time: (optional) How long to pause, in milliseconds.
    :attr bool typing: (optional) Whether to send a "user is typing" event during
          the pause.
    :attr str source: (optional) The URL of the image.
    :attr str title: (optional) The title or introductory text to show before the
          response.
    :attr str description: (optional) The description to show with the the response.
    :attr str preference: (optional) The preferred type of control to display.
    :attr List[DialogNodeOutputOptionsElement] options: (optional) An array of
          objects describing the options from which the user can choose.
    :attr str message_to_human_agent: (optional) A message to be sent to the human
          agent who will be taking over the conversation.
    :attr str topic: (optional) A label identifying the topic of the conversation,
          derived from the **user_label** property of the relevant node.
    :attr List[DialogSuggestion] suggestions: (optional) An array of objects
          describing the possible matching dialog nodes from which the user can choose.
          **Note:** The **suggestions** property is part of the disambiguation feature,
          which is only available for Premium users.
    :attr str header: (optional) The title or introductory text to show before the
          response. This text is defined in the search skill configuration.
    :attr List[SearchResult] results: (optional) An array of objects containing
          search results.
    """

    def __init__(self,
                 response_type: str,
                 *,
                 text: str = None,
                 time: int = None,
                 typing: bool = None,
                 source: str = None,
                 title: str = None,
                 description: str = None,
                 preference: str = None,
                 options: List['DialogNodeOutputOptionsElement'] = None,
                 message_to_human_agent: str = None,
                 topic: str = None,
                 suggestions: List['DialogSuggestion'] = None,
                 header: str = None,
                 results: List['SearchResult'] = None) -> None:
        """
        Initialize a RuntimeResponseGeneric object.

        :param str response_type: The type of response returned by the dialog node.
               The specified response type must be supported by the client application or
               channel.
               **Note:** The **suggestion** response type is part of the disambiguation
               feature, which is only available for Premium users.
        :param str text: (optional) The text of the response.
        :param int time: (optional) How long to pause, in milliseconds.
        :param bool typing: (optional) Whether to send a "user is typing" event
               during the pause.
        :param str source: (optional) The URL of the image.
        :param str title: (optional) The title or introductory text to show before
               the response.
        :param str description: (optional) The description to show with the the
               response.
        :param str preference: (optional) The preferred type of control to display.
        :param List[DialogNodeOutputOptionsElement] options: (optional) An array of
               objects describing the options from which the user can choose.
        :param str message_to_human_agent: (optional) A message to be sent to the
               human agent who will be taking over the conversation.
        :param str topic: (optional) A label identifying the topic of the
               conversation, derived from the **user_label** property of the relevant
               node.
        :param List[DialogSuggestion] suggestions: (optional) An array of objects
               describing the possible matching dialog nodes from which the user can
               choose.
               **Note:** The **suggestions** property is part of the disambiguation
               feature, which is only available for Premium users.
        :param str header: (optional) The title or introductory text to show before
               the response. This text is defined in the search skill configuration.
        :param List[SearchResult] results: (optional) An array of objects
               containing search results.
        """
        self.response_type = response_type
        self.text = text
        self.time = time
        self.typing = typing
        self.source = source
        self.title = title
        self.description = description
        self.preference = preference
        self.options = options
        self.message_to_human_agent = message_to_human_agent
        self.topic = topic
        self.suggestions = suggestions
        self.header = header
        self.results = results

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'RuntimeResponseGeneric':
        """Initialize a RuntimeResponseGeneric object from a json dictionary."""
        args = {}
        valid_keys = [
            'response_type', 'text', 'time', 'typing', 'source', 'title',
            'description', 'preference', 'options', 'message_to_human_agent',
            'topic', 'suggestions', 'header', 'results'
        ]
        bad_keys = set(_dict.keys()) - set(valid_keys)
        if bad_keys:
            raise ValueError(
                'Unrecognized keys detected in dictionary for class RuntimeResponseGeneric: '
                + ', '.join(bad_keys))
        if 'response_type' in _dict:
            args['response_type'] = _dict.get('response_type')
        else:
            raise ValueError(
                'Required property \'response_type\' not present in RuntimeResponseGeneric JSON'
            )
        if 'text' in _dict:
            args['text'] = _dict.get('text')
        if 'time' in _dict:
            args['time'] = _dict.get('time')
        if 'typing' in _dict:
            args['typing'] = _dict.get('typing')
        if 'source' in _dict:
            args['source'] = _dict.get('source')
        if 'title' in _dict:
            args['title'] = _dict.get('title')
        if 'description' in _dict:
            args['description'] = _dict.get('description')
        if 'preference' in _dict:
            args['preference'] = _dict.get('preference')
        if 'options' in _dict:
            args['options'] = [
                DialogNodeOutputOptionsElement._from_dict(x)
                for x in (_dict.get('options'))
            ]
        if 'message_to_human_agent' in _dict:
            args['message_to_human_agent'] = _dict.get('message_to_human_agent')
        if 'topic' in _dict:
            args['topic'] = _dict.get('topic')
        if 'suggestions' in _dict:
            args['suggestions'] = [
                DialogSuggestion._from_dict(x)
                for x in (_dict.get('suggestions'))
            ]
        if 'header' in _dict:
            args['header'] = _dict.get('header')
        if 'results' in _dict:
            args['results'] = [
                SearchResult._from_dict(x) for x in (_dict.get('results'))
            ]
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a RuntimeResponseGeneric object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'response_type') and self.response_type is not None:
            _dict['response_type'] = self.response_type
        if hasattr(self, 'text') and self.text is not None:
            _dict['text'] = self.text
        if hasattr(self, 'time') and self.time is not None:
            _dict['time'] = self.time
        if hasattr(self, 'typing') and self.typing is not None:
            _dict['typing'] = self.typing
        if hasattr(self, 'source') and self.source is not None:
            _dict['source'] = self.source
        if hasattr(self, 'title') and self.title is not None:
            _dict['title'] = self.title
        if hasattr(self, 'description') and self.description is not None:
            _dict['description'] = self.description
        if hasattr(self, 'preference') and self.preference is not None:
            _dict['preference'] = self.preference
        if hasattr(self, 'options') and self.options is not None:
            _dict['options'] = [x._to_dict() for x in self.options]
        if hasattr(self, 'message_to_human_agent'
                  ) and self.message_to_human_agent is not None:
            _dict['message_to_human_agent'] = self.message_to_human_agent
        if hasattr(self, 'topic') and self.topic is not None:
            _dict['topic'] = self.topic
        if hasattr(self, 'suggestions') and self.suggestions is not None:
            _dict['suggestions'] = [x._to_dict() for x in self.suggestions]
        if hasattr(self, 'header') and self.header is not None:
            _dict['header'] = self.header
        if hasattr(self, 'results') and self.results is not None:
            _dict['results'] = [x._to_dict() for x in self.results]
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this RuntimeResponseGeneric object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'RuntimeResponseGeneric') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'RuntimeResponseGeneric') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other

    class ResponseTypeEnum(Enum):
        """
        The type of response returned by the dialog node. The specified response type must
        be supported by the client application or channel.
        **Note:** The **suggestion** response type is part of the disambiguation feature,
        which is only available for Premium users.
        """
        TEXT = "text"
        PAUSE = "pause"
        IMAGE = "image"
        OPTION = "option"
        CONNECT_TO_AGENT = "connect_to_agent"
        SUGGESTION = "suggestion"
        SEARCH = "search"

    class PreferenceEnum(Enum):
        """
        The preferred type of control to display.
        """
        DROPDOWN = "dropdown"
        BUTTON = "button"


class SearchResult():
    """
    SearchResult.

    :attr str id: The unique identifier of the document in the Discovery service
          collection.
          This property is included in responses from search skills, which are a beta
          feature available only to Plus or Premium plan users.
    :attr SearchResultMetadata result_metadata: An object containing search result
          metadata from the Discovery service.
    :attr str body: (optional) A description of the search result. This is taken
          from an abstract, summary, or highlight field in the Discovery service response,
          as specified in the search skill configuration.
    :attr str title: (optional) The title of the search result. This is taken from a
          title or name field in the Discovery service response, as specified in the
          search skill configuration.
    :attr str url: (optional) The URL of the original data object in its native data
          source.
    :attr SearchResultHighlight highlight: (optional) An object containing segments
          of text from search results with query-matching text highlighted using HTML <em>
          tags.
    """

    def __init__(self,
                 id: str,
                 result_metadata: 'SearchResultMetadata',
                 *,
                 body: str = None,
                 title: str = None,
                 url: str = None,
                 highlight: 'SearchResultHighlight' = None) -> None:
        """
        Initialize a SearchResult object.

        :param str id: The unique identifier of the document in the Discovery
               service collection.
               This property is included in responses from search skills, which are a beta
               feature available only to Plus or Premium plan users.
        :param SearchResultMetadata result_metadata: An object containing search
               result metadata from the Discovery service.
        :param str body: (optional) A description of the search result. This is
               taken from an abstract, summary, or highlight field in the Discovery
               service response, as specified in the search skill configuration.
        :param str title: (optional) The title of the search result. This is taken
               from a title or name field in the Discovery service response, as specified
               in the search skill configuration.
        :param str url: (optional) The URL of the original data object in its
               native data source.
        :param SearchResultHighlight highlight: (optional) An object containing
               segments of text from search results with query-matching text highlighted
               using HTML <em> tags.
        """
        self.id = id
        self.result_metadata = result_metadata
        self.body = body
        self.title = title
        self.url = url
        self.highlight = highlight

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'SearchResult':
        """Initialize a SearchResult object from a json dictionary."""
        args = {}
        valid_keys = [
            'id', 'result_metadata', 'body', 'title', 'url', 'highlight'
        ]
        bad_keys = set(_dict.keys()) - set(valid_keys)
        if bad_keys:
            raise ValueError(
                'Unrecognized keys detected in dictionary for class SearchResult: '
                + ', '.join(bad_keys))
        if 'id' in _dict:
            args['id'] = _dict.get('id')
        else:
            raise ValueError(
                'Required property \'id\' not present in SearchResult JSON')
        if 'result_metadata' in _dict:
            args['result_metadata'] = SearchResultMetadata._from_dict(
                _dict.get('result_metadata'))
        else:
            raise ValueError(
                'Required property \'result_metadata\' not present in SearchResult JSON'
            )
        if 'body' in _dict:
            args['body'] = _dict.get('body')
        if 'title' in _dict:
            args['title'] = _dict.get('title')
        if 'url' in _dict:
            args['url'] = _dict.get('url')
        if 'highlight' in _dict:
            args['highlight'] = SearchResultHighlight._from_dict(
                _dict.get('highlight'))
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a SearchResult object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'id') and self.id is not None:
            _dict['id'] = self.id
        if hasattr(self,
                   'result_metadata') and self.result_metadata is not None:
            _dict['result_metadata'] = self.result_metadata._to_dict()
        if hasattr(self, 'body') and self.body is not None:
            _dict['body'] = self.body
        if hasattr(self, 'title') and self.title is not None:
            _dict['title'] = self.title
        if hasattr(self, 'url') and self.url is not None:
            _dict['url'] = self.url
        if hasattr(self, 'highlight') and self.highlight is not None:
            _dict['highlight'] = self.highlight._to_dict()
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this SearchResult object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'SearchResult') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'SearchResult') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class SearchResultHighlight():
    """
    An object containing segments of text from search results with query-matching text
    highlighted using HTML <em> tags.

    :attr List[str] body: (optional) An array of strings containing segments taken
          from body text in the search results, with query-matching substrings
          highlighted.
    :attr List[str] title: (optional) An array of strings containing segments taken
          from title text in the search results, with query-matching substrings
          highlighted.
    :attr List[str] url: (optional) An array of strings containing segments taken
          from URLs in the search results, with query-matching substrings highlighted.
    """

    def __init__(self,
                 *,
                 body: List[str] = None,
                 title: List[str] = None,
                 url: List[str] = None,
                 **kwargs) -> None:
        """
        Initialize a SearchResultHighlight object.

        :param List[str] body: (optional) An array of strings containing segments
               taken from body text in the search results, with query-matching substrings
               highlighted.
        :param List[str] title: (optional) An array of strings containing segments
               taken from title text in the search results, with query-matching substrings
               highlighted.
        :param List[str] url: (optional) An array of strings containing segments
               taken from URLs in the search results, with query-matching substrings
               highlighted.
        :param **kwargs: (optional) Any additional properties.
        """
        self.body = body
        self.title = title
        self.url = url
        for _key, _value in kwargs.items():
            setattr(self, _key, _value)

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'SearchResultHighlight':
        """Initialize a SearchResultHighlight object from a json dictionary."""
        args = {}
        xtra = _dict.copy()
        if 'body' in _dict:
            args['body'] = _dict.get('body')
            del xtra['body']
        if 'title' in _dict:
            args['title'] = _dict.get('title')
            del xtra['title']
        if 'url' in _dict:
            args['url'] = _dict.get('url')
            del xtra['url']
        args.update(xtra)
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a SearchResultHighlight object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'body') and self.body is not None:
            _dict['body'] = self.body
        if hasattr(self, 'title') and self.title is not None:
            _dict['title'] = self.title
        if hasattr(self, 'url') and self.url is not None:
            _dict['url'] = self.url
        if hasattr(self, '_additionalProperties'):
            for _key in self._additionalProperties:
                _value = getattr(self, _key, None)
                if _value is not None:
                    _dict[_key] = _value
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __setattr__(self, name: str, value: object) -> None:
        properties = {'body', 'title', 'url'}
        if not hasattr(self, '_additionalProperties'):
            super(SearchResultHighlight,
                  self).__setattr__('_additionalProperties', set())
        if name not in properties:
            self._additionalProperties.add(name)
        super(SearchResultHighlight, self).__setattr__(name, value)

    def __str__(self) -> str:
        """Return a `str` version of this SearchResultHighlight object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'SearchResultHighlight') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'SearchResultHighlight') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class SearchResultMetadata():
    """
    An object containing search result metadata from the Discovery service.

    :attr float confidence: (optional) The confidence score for the given result.
          For more information about how the confidence is calculated, see the Discovery
          service [documentation](../discovery#query-your-collection).
    :attr float score: (optional) An unbounded measure of the relevance of a
          particular result, dependent on the query and matching document. A higher score
          indicates a greater match to the query parameters.
    """

    def __init__(self, *, confidence: float = None,
                 score: float = None) -> None:
        """
        Initialize a SearchResultMetadata object.

        :param float confidence: (optional) The confidence score for the given
               result. For more information about how the confidence is calculated, see
               the Discovery service [documentation](../discovery#query-your-collection).
        :param float score: (optional) An unbounded measure of the relevance of a
               particular result, dependent on the query and matching document. A higher
               score indicates a greater match to the query parameters.
        """
        self.confidence = confidence
        self.score = score

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'SearchResultMetadata':
        """Initialize a SearchResultMetadata object from a json dictionary."""
        args = {}
        valid_keys = ['confidence', 'score']
        bad_keys = set(_dict.keys()) - set(valid_keys)
        if bad_keys:
            raise ValueError(
                'Unrecognized keys detected in dictionary for class SearchResultMetadata: '
                + ', '.join(bad_keys))
        if 'confidence' in _dict:
            args['confidence'] = _dict.get('confidence')
        if 'score' in _dict:
            args['score'] = _dict.get('score')
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a SearchResultMetadata object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'confidence') and self.confidence is not None:
            _dict['confidence'] = self.confidence
        if hasattr(self, 'score') and self.score is not None:
            _dict['score'] = self.score
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this SearchResultMetadata object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'SearchResultMetadata') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'SearchResultMetadata') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other


class SessionResponse():
    """
    SessionResponse.

    :attr str session_id: The session ID.
    """

    def __init__(self, session_id: str) -> None:
        """
        Initialize a SessionResponse object.

        :param str session_id: The session ID.
        """
        self.session_id = session_id

    @classmethod
    def from_dict(cls, _dict: Dict) -> 'SessionResponse':
        """Initialize a SessionResponse object from a json dictionary."""
        args = {}
        valid_keys = ['session_id']
        bad_keys = set(_dict.keys()) - set(valid_keys)
        if bad_keys:
            raise ValueError(
                'Unrecognized keys detected in dictionary for class SessionResponse: '
                + ', '.join(bad_keys))
        if 'session_id' in _dict:
            args['session_id'] = _dict.get('session_id')
        else:
            raise ValueError(
                'Required property \'session_id\' not present in SessionResponse JSON'
            )
        return cls(**args)

    @classmethod
    def _from_dict(cls, _dict):
        """Initialize a SessionResponse object from a json dictionary."""
        return cls.from_dict(_dict)

    def to_dict(self) -> Dict:
        """Return a json dictionary representing this model."""
        _dict = {}
        if hasattr(self, 'session_id') and self.session_id is not None:
            _dict['session_id'] = self.session_id
        return _dict

    def _to_dict(self):
        """Return a json dictionary representing this model."""
        return self.to_dict()

    def __str__(self) -> str:
        """Return a `str` version of this SessionResponse object."""
        return json.dumps(self._to_dict(), indent=2)

    def __eq__(self, other: 'SessionResponse') -> bool:
        """Return `true` when self and other are equal, false otherwise."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other: 'SessionResponse') -> bool:
        """Return `true` when self and other are not equal, false otherwise."""
        return not self == other
