"""
calm.py: automation to configure Calm for
NX-on-GCP / Test Drive.

Author: Michael Haigh (michael@nutanix.com)
Date: 2020-02-23
"""

import time
import sys
import os
import requests
import urllib3
import argparse
import getpass
import json

from base64 import b64encode
from requests.auth import HTTPBasicAuth

sys.path.append(os.path.join(os.getcwd(), "nutest_gcp.egg"))

from framework.lib.nulog import INFO, ERROR
from helpers.rest import (RequestParameters, PostRequestParameters,
     RequestResponse, RESTClient, PostRESTClient)


def create_v3_url(ip, endpoint):

  return f"https://{ip}:9440/api/nutanix/v3/{endpoint}"

def main():

  # Suppress Warnings
  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

  # Get and log the config from the Env variable
  config = json.loads(os.environ["CUSTOM_SCRIPT_CONFIG"])
  INFO(config)

  # Get PC info from the config dict
  pc_info = config.get("my_pc")
  pc_external_ip = pc_info.get("ips")[0][0]
  pc_internal_ip = pc_info.get("ips")[0][1]
  pc_password = pc_info.get("prism_password")

  try:

    # Make the API call
    parameters = PostRequestParameters(
          uri=create_v3_url(pc_external_ip, "projects/list"),
          username="admin",
          password=pc_password,
          payload="{}"
    )
    rest_client = PostRESTClient(parameters)
    prjlistresp = rest_client.post_request()

    print (type(prjlistresp))

    print(prjlistresp)

  except Exception as ex:
    print(ex)

if __name__ == '__main__':
  main()

