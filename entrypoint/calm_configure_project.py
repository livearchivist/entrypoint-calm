"""
calm_configure_project.py: automation to configure
Calm projects on NX-on-GCP / Test Drive.

Author: michael@nutanix.com
Date:   2020-02-24
"""

import sys
import os
import json
import traceback

from helpers.calm import (
    uuid_via_v3_post,
    body_via_v3_post,
    get_subnet_info,
    update_via_v3_put,
    file_to_dict,
)


def main():

    # Get and log the config from the Env variable
    config = json.loads(os.environ["CUSTOM_SCRIPT_CONFIG"])
    print(config)

    # Get PC info from the config dict
    pc_info = config.get("tdaas_pc")
    pc_external_ip = pc_info.get("ips")[0][0]
    pc_internal_ip = pc_info.get("ips")[0][1]
    pc_password = pc_info.get("prism_password")

    try:

        # Convert our spec to dict
        subnet_spec = file_to_dict("specs/calm_subnet.json")

        # Get our info from the infra
        subnet_info = get_subnet_info(
            pc_external_ip, pc_password, subnet_spec["entities"][0]["vlan"]
        )
        if "proxy_vm" in config:
            public_subnet_info = get_subnet_info(
                pc_external_ip, pc_password, subnet_spec["entities"][1]["vlan"]
            )
        account_info = body_via_v3_post(pc_external_ip, "accounts", pc_password, None)

        # Handle multiple environments
        env_body = body_via_v3_post(pc_external_ip, "environments", pc_password, None)
        for env in env_body.json["entities"]:
            if env["status"]["state"] == "ACTIVE":
                env_uuid = env["metadata"]["uuid"]
                break

        # Get the pojects body
        project_resp = body_via_v3_post(pc_external_ip, "projects", pc_password, None)

        # Loop through each project to add the env
        for project in project_resp.json["entities"]:

            # Delete the unneeded "status"
            del project["status"]

            # If default project, add subnet_ref_list
            if project["spec"]["name"] == "default":

                # add subnet if not present
                if len(project["spec"]["resources"]["subnet_reference_list"]) == 0:
                    project["spec"]["resources"]["subnet_reference_list"].append(
                        {
                            "kind": "subnet",
                            "name": subnet_info["name"],
                            "uuid": subnet_info["uuid"],
                        }
                    )
                    if "proxy_vm" in config:
                        project["spec"]["resources"]["subnet_reference_list"].append(
                            {
                                "kind": "subnet",
                                "name": public_subnet_info["name"],
                                "uuid": public_subnet_info["uuid"],
                            }
                        )

                # Add account if not present
                if len(project["spec"]["resources"]["account_reference_list"]) == 0:
                    for account in account_info.json["entities"]:
                        if account["status"]["resources"]["type"] == "nutanix_pc":
                            project["spec"]["resources"][
                                "account_reference_list"
                            ].append(
                                {
                                    "kind": "account",
                                    "name": account["metadata"]["name"],
                                    "uuid": account["metadata"]["uuid"],
                                }
                            )

            # Add env if not present, update if it is
            if len(project["spec"]["resources"]["environment_reference_list"]) == 0:
                project["spec"]["resources"]["environment_reference_list"].append(
                    {"kind": "environment", "uuid": env_uuid}
                )
            else:
                project["spec"]["resources"]["environment_reference_list"][0][
                    "uuid"
                ] = env_uuid

            # Make the API call to update the Project
            print(f"project: {project}")
            resp = update_via_v3_put(
                pc_external_ip,
                "projects",
                pc_password,
                project["metadata"]["uuid"],
                project,
            )

            # Log appropriately based on response
            if resp.code == 202 or resp.code == 200:
                print(f"{project['spec']['name']} Project updated successfully.")
            else:
                raise Exception(
                    f"{project['spec']['name']} Project update failed with:\n"
                    + f"Resp: {resp}\n"
                    + f"Error Code: {resp.code}\n"
                    + f"Error Message: {resp.message}"
                )

    except Exception as ex:
        print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
