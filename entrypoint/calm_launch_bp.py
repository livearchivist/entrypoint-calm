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
import traceback

from helpers.rest import RequestResponse
from helpers.calm import (
    file_to_dict,
    body_via_v3_post,
    body_via_v3_get,
    create_via_v3_post,
    recursive_dict_lookup,
)


def main(launch):

    # Get and log the config from the Env variable
    config = json.loads(os.environ["CUSTOM_SCRIPT_CONFIG"])
    print(config)

    # Get PC info from the config dict
    pc_info = config.get("tdaas_pc")
    pc_external_ip = pc_info.get("ips")[0][0]
    pc_internal_ip = pc_info.get("ips")[0][1]
    pc_password = pc_info.get("prism_password")

    try:

        # Read in the spec files and convert to dicts
        launch_spec = file_to_dict(f"specs/{launch}")
        print(f"launch_spec: {launch_spec}")

        # Loop through the blueprints to launch
        for launch in launch_spec["entities"]:

            # Get our blueprint uuid
            payload = {"filter": f"name=={launch['bp_name']}"}
            bp = body_via_v3_post(
                pc_external_ip, "blueprints", pc_password, payload
            ).json
            if bp["metadata"]["total_matches"] != 1:
                raise Exception(
                    str(bp["metadata"]["total_matches"])
                    + " blueprints found, when 1 should"
                    + " have been found."
                )
            else:
                bp_uuid = bp["entities"][0]["metadata"]["uuid"]

            # Get our runtime editables
            editables = body_via_v3_get(
                pc_external_ip,
                "blueprints",
                pc_password,
                bp_uuid + "/runtime_editables",
            ).json
            for profile in editables["resources"]:
                if profile["app_profile_reference"]["name"] == launch["profile_name"]:
                    profile_ref = profile["app_profile_reference"]
                    run_editables = profile["runtime_editables"]
            print(f"{launch['bp_name']} profile_ref: {profile_ref}")
            print(f"{launch['bp_name']} run_editables: {run_editables}")

            # Determine if this blueprint has an app dependency
            if "dependencies" in launch and len(launch["dependencies"]) > 0:
                # Get a list of running apps
                apps = body_via_v3_post(pc_external_ip, "apps", pc_password, None).json
                # Cycle through the apps
                for app in apps["entities"]:
                    # Cycle through our launch dependencies
                    for depend in launch["dependencies"]:
                        # Find the matching app name
                        if app["status"]["name"] == depend["app_name"]:
                            # Get app body
                            app_body = body_via_v3_get(
                                pc_external_ip,
                                "apps",
                                pc_password,
                                app["metadata"]["uuid"],
                            ).json
                            # Loop through our dependency values
                            for value in depend["values"]:
                                # Get value from our body+key combo
                                app_val = recursive_dict_lookup(app_body, value["keys"])
                                # Set our app_val to the appropriate variable value
                                for launch_var in launch["variables"]:
                                    if value["name"] == launch_var["name"]:
                                        launch_var["value"] = app_val
                print(f'{launch["bp_name"]} vars after depend: {launch["variables"]}')

            # Set our runtime variables
            if "variable_list" in run_editables:
                for run_edit_var in run_editables["variable_list"]:
                    for launch_var in launch["variables"]:
                        if run_edit_var["name"] == launch_var["name"]:
                            run_edit_var["value"]["value"] = launch_var["value"]
                print(f"{launch['bp_name']} run_editables: {run_editables}")

            # Create our payload and launch our app
            payload = {
                "spec": {
                    "app_name": launch["app_name"],
                    "app_description": launch["app_description"],
                    "app_profile_reference": profile_ref,
                    "runtime_editables": run_editables,
                }
            }
            resp = create_via_v3_post(
                pc_external_ip,
                "blueprints/" + bp_uuid + "/simple_launch",
                pc_password,
                payload,
            )

            # Log appropriately based on response
            if resp.code == 200 or resp.code == 202:
                print(f"{launch['app_name']} app launched successfully.")
            else:
                raise Exception(
                    f"{launch['app_name']} app launch failed with:\n"
                    + f"Resp: {resp}\n"
                    + f"Error Code: {resp.code}\n"
                    + f"Error Message: {resp.message}"
                )

            time.sleep(2)

    except Exception as ex:
        print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    for launch_spec in sys.argv:
        if not launch_spec.endswith("py"):
            main(launch_spec)

