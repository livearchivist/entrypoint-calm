"""
calm_create_image.py: automation to create a
Calm Project on NX-on-GCP / Test Drive.

Author: michael@nutanix.com
Date:   2020-02-28
"""

import sys
import os
import json
import uuid

sys.path.append(os.path.join(os.getcwd(), "nutest_gcp.egg"))

from framework.lib.nulog import INFO, ERROR
from helpers.rest import RequestResponse
from helpers.calm import (file_to_dict, create_via_v3_post,
                          uuid_via_v3_post, body_via_v3_get,
                          body_via_v3_post)


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
    project_spec = file_to_dict("calm_project.spec")
    INFO(f"image_spec: {project_spec}")

    # Get our subnet info from the infra
    subnets_body = body_via_v3_post(pc_external_ip, "subnets",
                                   pc_password)
    for subnet in subnets_body.json['entities']:
      if subnet["spec"]["resources"]["vlan_id"] == 1:
        subnet_name = subnet["spec"]["name"]
        subnet_uuid = subnet["metadata"]["uuid"]
        
    # Update our project_spec
    project_spec["spec"]["name"] = "NY_Office" #TODO: parameterize
    project_spec["spec"]["resources"]["subnet_reference_list"][0]\
                ["name"] = subnet_name
    project_spec["spec"]["resources"]["subnet_reference_list"][0]\  
                ["uuid"] = subnet_uuid

    # Make API call to create image
    resp = create_via_v3_post(pc_external_ip, "projects",
                              pc_password, project_spec)

    # Log appropriately based on response
    if resp.code == 202:
      INFO(f"{project_spec['spec']['name']} Project created successfully.")
    else:
      raise Exception(f"{project_spec['spec']['name']} Project create" +
                      f" failed with:\n" +
                      f"Error Code: {resp.code}\n" +
                      f"Error Message: {resp.message}")

  except Exception as ex:
    INFO(ex)

if __name__ == '__main__':
  main()
