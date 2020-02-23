"""
rest.py: Rest API helper classes
"""

import requests
import urllib3
import argparse
import getpass
import json

from base64 import b64encode
from requests.auth import HTTPBasicAuth


class RequestParameters:
    """
    class to hold the parameters of our API request
    this is not strictly required but can make
    our requests cleaner
    """

    def __init__(self, uri, username, password):
        self.uri = uri
        self.username = username
        self.password = password

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'uri={self.uri},'
                f'username={self.username},'
                f'password={self.password})')


class PostRequestParameters: 
    """
    class to hold the parameters of our API request
    this is not strictly required but can make
    our requests cleaner
    """

    def __init__(self, uri, username, password, payload):
        self.uri = uri
        self.username = username
        self.password = password
        self.payload = payload

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'uri={self.uri},'
                f'username={self.username},'
                f'password={self.password},'
                f'payload={self.payload})')

class RequestResponse:
    """
    class to hold the response from our
    requests
    again, not strictly necessary but can
    make things cleaner later
    """

    def __init__(self):
        self.code = 0
        self.message = ""
        self.json = ""
        self.details = ""

    def __repr__(self):
        '''
        decent __repr__ for debuggability
        this is something recommended by Raymond Hettinger
        it is good practice and should be left here
        unless there's a good reason to remove it
        '''
        return (f'{self.__class__.__name__}('
                f'code={self.code},'
                f'message={self.message},'
                f'json={self.json},'
                f'details={self.details})')

class RESTClient:
    """
    the RESTClient class carries out the actual API request
    by 'packaging' these functions into a dedicated class,
    we can re-use instances of this class, resulting in removal
    of unnecessary code repetition and resources
    """

    def __init__(self, parameters: RequestParameters):
        """
        class constructor
        because this is a simple class, we only have a single
        instance variable, 'params', that holds the parameters
        relevant to this request
        """
        self.params = parameters

    def get_request(self):
        """
        this is the main method that carries out the request
        basic exception handling is managed here, as well as
        returning the response (success or fail), as an instance
        of our RequestResponse dataclass
        """
        response = RequestResponse()

        """
        setup the HTTP Basic Authorization header based on the
        supplied username and password
        done this way so that passwords are not supplied on the command line
        """
        username = self.params.username
        password = self.params.password
        encoded_credentials = b64encode(
            bytes(f"{username}:{password}", encoding="ascii")
        ).decode("ascii")
        auth_header = f"Basic {encoded_credentials}"

        """
        setup the request headers
        note the use of {auth_header} i.e. the Basic Authorization
        credentials we setup earlier
        """

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"{auth_header}",
            "cache-control": "no-cache",
        }

        try:
            # submit the request
            api_request = requests.get(
                self.params.uri,
                headers=headers,
                auth=HTTPBasicAuth(username, password),
                timeout=30,
                verify=False
            )
            # if no exceptions occur here, we can process the response
            response.code = api_request.status_code
            response.message = "Request submitted successfully."
            response.json = api_request.json()
            response.details = "N/A"
        except requests.exceptions.ConnectTimeout:
            # timeout while connecting to the specified IP address or FQDN
            response.code = -99
            response.message = f"Connection has timed out. {username} {password}"
            response.details = "Exception: requests.exceptions.ConnectTimeout"
        except urllib3.exceptions.ConnectTimeoutError:
            # timeout while connecting to the specified IP address or FQDN
            response.code = -99
            response.message = f"Connection has timed out."
            response.details = "urllib3.exceptions.ConnectTimeoutError"
        except requests.exceptions.MissingSchema:
            # potentially bad URL
            response.code = -99
            response.message = "Missing URL schema/bad URL."
            response.details = "N/A"
        except Exception as _e:
            """
            unhandled exception
            ... don't do this in production
            """
            response.code = -99
            response.message = "An unhandled exception has occurred."
            response.details = _e

        return response

class PostRESTClient:
    """
    the RESTClient class carries out the actual API request
    by 'packaging' these functions into a dedicated class,
    we can re-use instances of this class, resulting in removal
    of unnecessary code repetition and resources
    """

    def __init__(self, parameters: PostRequestParameters):
        """
        class constructor
        because this is a simple class, we only have a single
        instance variable, 'params', that holds the parameters
        relevant to this request
        """
        self.params = parameters

    def post_request(self):
        """
        this is the main method that carries out the request
        basic exception handling is managed here, as well as
        returning the response (success or fail), as an instance
        of our RequestResponse dataclass
        """
        response = RequestResponse()

        """
        setup the HTTP Basic Authorization header based on the
        supplied username and password
        done this way so that passwords are not supplied on the command line
        """
        username = self.params.username
        password = self.params.password
        encoded_credentials = b64encode(
            bytes(f"{username}:{password}", encoding="ascii")
        ).decode("ascii")
        auth_header = f"Basic {encoded_credentials}"
        

        """
        setup the request headers
        note the use of {auth_header} i.e. the Basic Authorization
        credentials we setup earlier
        """

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"{auth_header}",
            "cache-control": "no-cache",
        }

        try:
            # submit the request
            api_request = requests.post(
                self.params.uri,
                data=self.params.payload,
                headers=headers,
                verify=False,
                timeout=10,
            )

            '''auth=HTTPBasicAuth(username, password),'''
            # if no exceptions occur here, we can process the response
            response.code = api_request.status_code
            response.message = "Request submitted successfully."
            response.json = api_request.json()
            response.details = "N/A"
        except requests.exceptions.ConnectTimeout:
            # timeout while connecting to the specified IP address or FQDN
            response.code = -99
            response.message = f"Connection has timed out. {username} {password}"
            response.details = "Exception: requests.exceptions.ConnectTimeout"
        except urllib3.exceptions.ConnectTimeoutError:
            # timeout while connecting to the specified IP address or FQDN
            response.code = -99
            response.message = f"Connection has timed out."
            response.details = "urllib3.exceptions.ConnectTimeoutError"
        except requests.exceptions.MissingSchema:
            # potentially bad URL
            response.code = -99
            response.message = "Missing URL schema/bad URL."
            response.details = "N/A"
        except Exception as _e:
            """
            unhandled exception
            ... don't do this in production
            """
            response.code = -99
            response.message = "An unhandled exception has occurred."
            response.details = _e

        return response

