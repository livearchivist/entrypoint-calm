"""
calm_upload_bp.py: automation to upload
blueprints on NX-on-GCP / Test Drive.

Author: michael@nutanix.com
Date:   2020-03-05
"""

import sys
import os
import json

sys.path.append(os.path.join(os.getcwd(), "nutest_gcp.egg"))

from framework.lib.nulog import INFO, ERROR
from helpers.rest import RequestResponse
from helpers.calm import (file_to_dict, uuid_via_v3_post,
                          upload_bp_via_v3_post)

def main():

  # Get and log the config from the Env variable
  config = json.loads(os.environ["CUSTOM_SCRIPT_CONFIG"])
  INFO(config)

  # Get PC info from the config dict
  pc_info = config.get("tdaas_pc")
  pc_external_ip = pc_info.get("ips")[0][0]
  pc_internal_ip = pc_info.get("ips")[0][1]
  pc_password = pc_info.get("prism_password")

  try:

    # Read in the spec files and conver to dicts
    bp_spec = file_to_dict("specs/calm_bp_upload.json")
    INFO(f"bp_spec: {bp_spec}")

    # Loop through the blueprints to upload
    for bp in bp_spec["entities"]:

      # Get our project uuid and create our payload
      project_uuid = uuid_via_v3_post(pc_external_ip, "projects",
                                      pc_password, bp["bp_project"])
      payload = {
        "name": bp["bp_name"],
        "project_uuid": project_uuid
      }

      # Upload our blueprint
      resp = upload_bp_via_v3_post(pc_external_ip, pc_password,
                                   payload, bp["bp_file"])

      # Log appropriately based on response
      if (resp.code == 200 or resp.code == 202):
        INFO(f"{bp['bp_name']} blueprint created successfully.")
      else:
        raise Exception(f"{bp['bp_name']} blueprint create" +
                        f" failed with:\n" +
                        f"Error Code: {resp.code}\n" +
                        f"Error Message: {resp.message}")

  except Exception as ex:
    INFO(ex)

if __name__ == '__main__':
  main()

