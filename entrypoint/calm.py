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

sys.path.append(os.path.join(os.getcwd(), "nutest_gcp.egg"))

from framework.lib.nulog import INFO, ERROR
from helpers.rest import (RequestParameters, PostRequestParameters,
     RequestResponse, RESTClient, PostRESTClient)


def create_v3_url(ip, endpoint):

  return f"https://{ip}:9440/api/nutanix/v3/{endpoint}"

def main():

  # Get and log the config from the Env variable
  config = json.loads(os.environ["CUSTOM_SCRIPT_CONFIG"])
  INFO(config)

  # Get PC info from the config dict
  pc_info = config.get("my_pc")
  pc_external_ip = pc_info.get("ips")[0][0]
  pc_internal_ip = pc_info.get("ips")[0][1]
  pc_password = pc_info.get("prism_password")


  parameters = RequestParameters(
        uri="url",
        username="admin",
        password="password"
  )

  print(create_v3_url(pc_external_ip, "projects"))

if __name__ == '__main__':
  main()

