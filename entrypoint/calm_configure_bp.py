"""
calm_configure_bp.py: automation to configure
blueprints on NX-on-GCP / Test Drive.

Author: michael@nutanix.com
Date:   2020-03-09
"""

import sys
import os
import json

sys.path.append(os.path.join(os.getcwd(), "nutest_gcp.egg"))

from framework.lib.nulog import INFO, ERROR
from helpers.rest import RequestResponse
from helpers.calm import (file_to_dict, get_subnet_info
                          body_via_v3_get, update_via_v3_put)

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
    subnet_spec = file_to_dict("calm_subnet.spec")
    INFO(f"subnet_spec: {subnet_spec}")
    #bp_spec = file_to_dict("calm_bp_upload.spec")
    #INFO(f"bp_spec: {bp_spec}")
    key_spec = file_to_dict("calm_userkey.spec")
    INFO(f"userkey_spec: {key_spec}")
    pass_spec = file_to_dict("calm_userpassword.spec")
    INFO(f"userpass_spec: {pass_spec}")

    # Get our subnet info from the infra
    subnet_info = get_subnet_info(pc_external_ip, pc_password,
                                  subnet_spec["vlan"])

    # Get a list of DRAFT blueprints
    payload = {
      "filter": "state==DRAFT"
    }
    draft_resp = body_via_v3_post(pc_external_ip, "blueprints",
                                  pc_password, payload)

    # Loop through the blueprints to modify
    for bp in draft_resp["entities"]:

      # Get the body of our blueprint
      bp_body = body_via_v3_get(pc_external_ip, "blueprints",
                                pc_password, bp["metadata"]["uuid"])

      # Remove unneeded status
      del bp_body["status"]

      # Configure secrets
      for secret in bp_body["spec"]["resources"]["credential_definition_list"]:
        #TODO: add conditional based on secret type
        secret["secret"]["attrs"]["is_secret_modified"] = True
        #TODO: Add username
        secret["secret"]["value"] = key_spec["secret"]
        print(json.dumps(secret, sort_keys=True, indent=4))

      # Configure NICs
      for substrate in bp_body["spec"]["resources"]["substrate_definition_list"]:
        if substrate["type"] == "AHV_VM":
          for nic in substrate["create_spec"]["resources"]["nic_list"]:
            nic["subnet_reference"]["uuid"] = subnet_info["uuid"]
            nic["subnet_reference"]["name"] = subnet_info["name"]
            print(json.dumps(nic, sort_keys=True, indent=4))

      # Update our blueprint
      resp = update_via_v3_put(pc_ip, "blueprints", pc_password,
                               bp["metadata"]["uuid"], bp_body)

      # Log appropriately based on response
      if (resp.code == 200 or resp.code == 202):
        INFO(f"{bp['metadata']['name']} blueprint updated successfully.")
      else:
        raise Exception(f"{bp['metadata']['name']} blueprint update" +
                        f" failed with:\n" +
                        f"Error Code: {resp.code}\n" +
                        f"Error Message: {resp.message}")

  except Exception as ex:
    INFO(ex)

if __name__ == '__main__':
  main()

