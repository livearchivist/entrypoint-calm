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


# Given an IP and Endpoint, return Nutanix v3 API URL
def create_v3_url(ip, endpoint):

  return f"https://{ip}:9440/api/nutanix/v3/{endpoint}"


# Return the UUID of a desired entity.  If entity_name is empty
# assume a single entity in response and send first UUID
def get_uuid_via_v3_post(ip, endpoint, password, entity_name):

  # Make the API call
  parameters = PostRequestParameters(
          uri=create_v3_url(ip, "projects/list"),
          username="admin",
          password=password,
          payload="{'length': 100}"
    )
  rest_client = PostRESTClient(parameters)
  resp = rest_client.post_request()
  INFO(resp)

  # Return UUID
  for entity in resp.json["entities"]:
    if entity_name == "":
      return entity["metadata"]["uuid"]
    elif entity["spec"]["name"] == entity_name:
      return entity["metadata"]["uuid"]


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

    # Get "default" project UUID
    project_uuid = get_uuid_via_v3_post(pc_external_ip,"projects/list",
                                        pc_password, "default")
    INFO(project_uuid)

    # Get the single account UUID
    account_uuid = get_uuid_via_v3_post(pc_external_ip,"accounts/list",
                                        pc_password, "")
    INFO(account_uuid)

    # Make the projects Get
    parameters = RequestParameters(
          uri=create_v3_url(pc_external_ip, f"projects/{project_uuid}"),
          username="admin",
          password=pc_password
    )
    rest_client = RESTClient(parameters)
    project_get_resp = rest_client.get_request()
    INFO(project_get_resp)

    # Get the project body, delete unneeded status
    project_body = project_get_resp.json
    del project_body["status"]
    INFO(project_body)

  except Exception as ex:
    print(ex)

if __name__ == '__main__':
  main()

