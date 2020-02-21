import sys
import os
import json
import time
import requests
import urllib3
import argparse
import getpass

from base64 import b64encode
from requests.auth import HTTPBasicAuth

from helpers.rest import (RequestParameters, PostRequestParameters,
     RequestResponse, RESTClient, PostRESTClient)

def main():

  parameters = RequestParameters(
        uri="url",
        username="admin",
        password="password"
  )

  print("Success!")

if __name__ == '__main__':
  main()

