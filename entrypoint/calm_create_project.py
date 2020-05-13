"""
calm_create_project.py: automation to create a
Calm Project on NX-on-GCP / Test Drive.

Author: michael@nutanix.com
Date:   2020-02-28
"""

import sys
import os
import json
import traceback

from helpers.rest import RequestResponse
from helpers.calm import (
    file_to_dict,
    create_via_v3_post,
    get_subnet_info,
    body_via_v3_post,
)


def main(project_name):

    # Get and log the config from the Env variable
    config = json.loads(os.environ["CUSTOM_SCRIPT_CONFIG"])
    print(config)

    # Get PC info from the config dict
    pc_info = config.get("tdaas_pc")
    pc_external_ip = pc_info.get("ips")[0][0]
    pc_internal_ip = pc_info.get("ips")[0][1]
    pc_password = pc_info.get("prism_password")

    try:

        # Read in the spec files and conver to dicts
        project_spec = file_to_dict("specs/calm_project.json")
        print(f"project_spec pre-update: {project_spec}")
        subnet_spec = file_to_dict("specs/calm_subnet.json")
        print(f"subnet_spec pre-update: {subnet_spec}")

        # Get our info from the infra
        subnet_info = get_subnet_info(
            pc_external_ip, pc_password, subnet_spec["entities"][0]["vlan"]
        )
        account_info = body_via_v3_post(pc_external_ip, "accounts", pc_password, None)

        # Cycle through our accounts to find the right one
        for account in account_info.json["entities"]:
            if account["status"]["resources"]["type"] == "nutanix_pc":

                # Update our project_spec
                project_spec["spec"]["name"] = project_name
                project_spec["spec"]["resources"]["subnet_reference_list"][0][
                    "name"
                ] = subnet_info["name"]
                project_spec["spec"]["resources"]["subnet_reference_list"][0][
                    "uuid"
                ] = subnet_info["uuid"]
                project_spec["spec"]["resources"]["account_reference_list"][0][
                    "name"
                ] = account["metadata"]["name"]
                project_spec["spec"]["resources"]["account_reference_list"][0][
                    "uuid"
                ] = account["metadata"]["uuid"]
                print(f"project_spec post-update: {project_spec}")

                # Make API call to create project
                resp = create_via_v3_post(
                    pc_external_ip, "projects", pc_password, project_spec
                )

                # Log appropriately based on response
                if resp.code == 200 or resp.code == 202:
                    print(
                        f"{project_spec['spec']['name']} Project created successfully."
                    )
                else:
                    raise Exception(
                        f"{project_spec['spec']['name']} Project create"
                        + f" failed with:\n"
                        + f"Error Code: {resp.code}\n"
                        + f"Error Message: {resp.message}"
                    )

    except Exception as ex:
        print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    for project in sys.argv:
        if not project.endswith("py"):
            main(project)

