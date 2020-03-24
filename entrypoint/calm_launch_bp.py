"""
calm_launch_bp.py: automation to launch
blueprints on NX-on-GCP / Test Drive.

Author: michael@nutanix.com
Date:   2020-03-18
"""

import sys
import os
import json
import time

sys.path.append(os.path.join(os.getcwd(), "nutest_gcp.egg"))

from framework.lib.nulog import INFO, ERROR
from helpers.rest import RequestResponse
from helpers.calm import (file_to_dict, body_via_v3_post,
                          body_via_v3_get, create_via_v3_post)


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

    # Read in the spec files and convert to dicts
    launch_spec = file_to_dict("specs/calm_bp_launch.spec")
    INFO(f"launch_spec: {launch_spec}")

    # Loop through the blueprints to launch
    for launch in launch_spec["entities"]:

      # Get our blueprint uuid
      payload = {
        "filter": f"name=={launch['bp_name']}"
      }
      bp = body_via_v3_post(pc_external_ip, "blueprints",
                            pc_password, payload).json
      if bp["metadata"]["total_matches"] != 1:
        raise Exception(str(bp["metadata"]["total_matches"]) +
                        " blueprints found, when 1 should" +
                        " have been found.")
      else:
        bp_uuid = bp["entities"][0]["metadata"]["uuid"]

      # Get our runtime editables
      editables = body_via_v3_get(pc_external_ip, "blueprints",
                                  pc_password,
                                  bp_uuid + "/runtime_editables").json
      for profile in editables["resources"]:
        if profile["app_profile_reference"]["name"] ==\
           launch["profile_name"]:
          profile_ref = profile["app_profile_reference"]
          run_editables = profile["runtime_editables"]
      INFO(f"{launch['bp_name']} profile_ref: {profile_ref}")
      INFO(f"{launch['bp_name']} run_editables: {run_editables}")

      # Set our runtime variables
      if "variable_list" in run_editables:
        for run_edit_var in run_editables["variable_list"]:
          for launch_var in launch["variables"]:
            if run_edit_var["name"] == launch_var["name"]:
              run_edit_var["value"]["value"] = launch_var["value"]
        INFO(f"{launch['bp_name']} run_editables: {run_editables}")

      # Create our payload and launch our app
      payload = {
        "spec": {
          "app_name": launch["app_name"],
          "app_description": launch["app_description"],
          "app_profile_reference": profile_ref,
          "runtime_editables": run_editables
        }
      }
      resp = create_via_v3_post(pc_external_ip,
                                "blueprints/" + bp_uuid + "/simple_launch",
                                pc_password, payload)

      # Log appropriately based on response
      if (resp.code == 200 or resp.code == 202):
        INFO(f"{launch['app_name']} app launched successfully.")
      else:
        raise Exception(f"{launch['app_name']} app launch" +
                        f" failed with:\n" +
                        f"Error Code: {resp.code}\n" +
                        f"Error Message: {resp.message}")

      time.sleep(2)

  except Exception as ex:
    INFO(ex)

if __name__ == '__main__':
  main()

