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

    # Make the projects/list Post
    parameters = PostRequestParameters(
          uri=create_v3_url(pc_external_ip, "projects/list"),
          username="admin",
          password=pc_password,
          payload="{}"
    )
    rest_client = PostRESTClient(parameters)
    project_list_resp = rest_client.post_request()

    # Get "default" project UUID
    for entity in project_list_resp.json["entities"]:
      if entity["spec"]["name"] == "default":
        project_uuid = entity["metadata"]["uuid"]

    # Make the projects Get
    parameters = RequestParameters(
          uri=create_v3_url(pc_external_ip, f"projects/{project_uuid}"),
          username="admin",
          password=pc_password
    )
    rest_client = RESTClient(parameters)
    project_get_resp = rest_client.get_request()

    # Get the project body, delete unneeded status
    project_body = project_get_resp.json
    del project_body["status"]

    print(project_body)

  except Exception as ex:
    print(ex)

if __name__ == '__main__':
  main()

