"""
calm_configure_project.py: automation to configure
Calm projects on NX-on-GCP / Test Drive.

Author: michael@nutanix.com
Date:   2020-02-24
"""

import sys
import os
import json

sys.path.append(os.path.join(os.getcwd(), "nutest_gcp.egg"))

from framework.lib.nulog import INFO, ERROR
from helpers.calm import (uuid_via_v3_post, body_via_v3_post,
                          get_subnet_info, update_via_v3_put,
                          file_to_dict)


def main():

  # Get and log the config from the Env variable
  config = json.loads(os.environ["CUSTOM_SCRIPT_CONFIG"])
  INFO(config)

  # Get PC info from the config dict
  pc_info = config.get("tdaas_pc")
  pc_external_ip = pc_info.get("ips")[0][0]
  pc_internal_ip = pc_info.get("ips")[0][1]
  pc_password = pc_info.get("password")

  try:

    # Convert our spec to dict
    subnet_spec = file_to_dict("calm_subnet.spec")

    # Get our subnet info from the infra
    subnet_info = get_subnet_info(pc_external_ip, pc_password,
                                  subnet_spec["vlan"])
    INFO(f"subnet_uuid: {subnet_info['uuid']}")

    # Get our only env uuid from the infra
    env_uuid = uuid_via_v3_post(pc_external_ip, "environments",
                                pc_password, "")

    # Get the pojects body
    project_resp = body_via_v3_post(pc_external_ip, "projects",
                                    pc_password)

    # Loop through each project to add the env
    for project in project_resp.json["entities"]:

      # Delete the unneeded "status"
      del project["status"]

      # If default project, add subnet_ref_list
      if project["spec"]["name"] == "default":
        project["spec"]["resources"]["subnet_reference_list"].append(
          {
            "kind": "subnet",
            "name": subnet_info["name"],
            "uuid": subnet_info["uuid"]
          }
        )

      # Add environment to all projects
      project["spec"]["resources"]["environment_reference_list"].append(
        {
          "kind": "environment",
          "uuid": env_uuid
        }
      )

      # Make the API call to update the Project
      INFO(f"project: {project}")
      resp = update_via_v3_put(pc_external_ip, "projects", pc_password,
                               project["metadata"]["uuid"], project)

      # Log appropriately based on response
      if (resp.code == 202 or resp.code == 200):
        INFO(f"{project['spec']['name']} Project updated successfully.")
      else:
        raise Exception(f"{project['spec']['name']} Project update" +
                        f" failed with:\n" +
                        f"Error Code: {resp.code}\n" +
                        f"Error Message: {resp.message}")

  except Exception as ex:
    print(ex)

if __name__ == '__main__':
  main()

