"""
calm_configure_project.py: automation to configure the default
Calm project on NX-on-GCP / Test Drive.

Author: michael@nutanix.com
Date:   2020-02-24
"""

import sys
import os
import json

sys.path.append(os.path.join(os.getcwd(), "nutest_gcp.egg"))

from framework.lib.nulog import INFO, ERROR
from helpers.calm import (uuid_via_v3_post, body_via_v3_get)


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

    # Get "default" project UUID
    project_uuid = uuid_via_v3_post(pc_external_ip, "projects",
                                    pc_password, "default")
    INFO(f"default_project_uuid: {project_uuid}")

    # Get the single account UUID
    account_uuid = uuid_via_v3_post(pc_external_ip, "accounts",
                                    pc_password, "")
    INFO(f"account_uuid: {account_uuid}")

    # Get the single subnets UUID
    subnet_uuid = uuid_via_v3_post(pc_external_ip, "subnets",
                                   pc_password, "")
    INFO(f"subnet_uuid: {subnet_uuid}")

    # Get the pojects body, delete status
    project_body = body_via_v3_get(pc_external_ip, "projects",
                                       pc_password, project_uuid)
    del project_body["status"]
    INFO(f"project_body: {project_body}")

    # Added resources to projects body
    project_body["spec"]["resources"]["account_reference_list"] = [
        {
            "kind": "account",
            "uuid": account_uuid
        }
    ]
    # TODO: Is there a better way than hardcoding the 'default-net' name?
    project_body["spec"]["resources"]["subnet_reference_list"] = [
        {
            "kind": "subnet",
            "name": "default-net",
            "uuid": subnet_uuid
        }
    ]
    project_body["spec"]["resources"]["default_subnet_reference"] = {
        "kind": "subnet",
        "uuid": subnet_uuid
    }

    INFO(f"project_body: {project_body}")

    # TODO: Make an API call to update Project

  except Exception as ex:
    print(ex)

if __name__ == '__main__':
  main()

