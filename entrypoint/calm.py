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
          uri=create_v3_url(ip, f"{endpoint}/list"),
          username="admin",
          password=password,
          payload="{\"length\": 100}"
    )
  rest_client = PostRESTClient(parameters)
  resp = rest_client.post_request()
  INFO(f"get_uuid_via_v3_post: {ip}, {endpoint}, {entity_name}:\nresp")

  # Return UUID
  for entity in resp.json["entities"]:
    if entity_name == "":
      return entity["metadata"]["uuid"]
    elif entity["spec"]["name"] == entity_name:
      return entity["metadata"]["uuid"]


# Return the body of a desired entity
def get_body_via_v3_get(ip, endpoint, password, entity_uuid):

  # Make the API call
  parameters = RequestParameters(
        uri=create_v3_url(ip, f"{endpoint}/{entity_uuid}"),
        username="admin",
        password=pc_password
  )
  rest_client = RESTClient(parameters)
  resp = rest_client.get_request()
  INFO(f"get_body_via_v3_get: {ip}, {endpoint}, {entity_uuid}:\nresp")

  # Get the body, delete unneeded status, return body
  body = project_get_resp.json
  del body["status"]
  return body


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
    project_uuid = get_uuid_via_v3_post(pc_external_ip, "projects/list",
                                        pc_password, "default")
    INFO(f"default_project_uuid: {project_uuid}")

    # Get the single account UUID
    account_uuid = get_uuid_via_v3_post(pc_external_ip, "accounts/list",
                                        pc_password, "")
    INFO(f"account_uuid: {account_uuid}")

    # Make the projects Get
    # Get the pojects body
    project_body = get_body_via_v3_get(pc_external_ip, "projects",
                                       pc_password, project_uuid)
    INFO(f"project_body: {project_body}")

  except Exception as ex:
    print(ex)

if __name__ == '__main__':
  main()

