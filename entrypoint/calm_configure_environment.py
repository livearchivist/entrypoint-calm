"""
calm_configure_environment.py: automation to configure a
Calm environment on NX-on-GCP / Test Drive.

Author: michael@nutanix.com
Date:   2020-02-24
"""

import sys
import os
import json
import uuid

sys.path.append(os.path.join(os.getcwd(), "nutest_gcp.egg"))

from framework.lib.nulog import INFO, ERROR
from helpers.calm import (file_to_dict, uuid_via_v3_post,
                          body_via_v3_get)


def main():

  # Get and log the config from the Env variable
  config = json.loads(os.environ["CUSTOM_SCRIPT_CONFIG"])
  INFO(config)

  # Get PC info from the config dict
  pc_info = config.get("my_pc")
  pc_external_ip = pc_info.get("ips")[0][0]
  pc_internal_ip = pc_info.get("ips")[0][1]
  pc_password = pc_info.get("prism_password")

  try:

    # Read in the spec file and conver to dict
    env_spec = file_to_dict("calm_environment.spec")

    # Get UUIDs from infra components
    account_uuid = uuid_via_v3_post(pc_external_ip, "accounts",
                                    pc_password, "")
    INFO(f"account_uuid: {account_uuid}")
    subnet_uuid = uuid_via_v3_post(pc_external_ip, "subnets",
                                   pc_password, "")
    INFO(f"subnet_uuid: {subnet_uuid}")

    # Need to create image

    # Apply random UUIDs to 

  except Exception as ex:
    INFO(ex)

if __name__ == '__main__':
  main()
