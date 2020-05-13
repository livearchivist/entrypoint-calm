"""
calm_configure_bp.py: automation to configure
blueprints on NX-on-GCP / Test Drive.

Author: michael@nutanix.com
Date:   2020-03-09
"""

import sys
import os
import json
import traceback

from helpers.rest import RequestResponse
from helpers.calm import (
    file_to_dict,
    get_subnet_info,
    body_via_v3_get,
    body_via_v3_post,
    update_via_v3_put,
    create_proxy_array,
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

    # Get PE info from the config dict
    pe_info = config.get("tdaas_cluster")
    pe_external_ip = pe_info.get("ips")[0][0]
    pe_internal_ip = pe_info.get("ips")[0][1]
    pe_password = pe_info.get("prism_password")

    try:

        # Read in the spec files and conver to dicts
        subnet_spec = file_to_dict("specs/calm_subnet.json")
        print(f"subnet_spec: {subnet_spec}")
        secret_spec = file_to_dict("specs/calm_secrets.json")
        print(f"secret_spec: {secret_spec}")

        # Get our subnet and image info from the infra
        subnet_info = get_subnet_info(
            pc_external_ip, pc_password, subnet_spec["entities"][0]["vlan"]
        )
        infra_subnet_info = get_subnet_info(
            pc_external_ip, pc_password, subnet_spec["entities"][1]["vlan"]
        )
        image_info = body_via_v3_post(pc_external_ip, "images", pc_password, None).json

        # If we have Public UVMs / Proxy IPs, then get our array
        proxy_array = []
        if "proxy_vm" in config:
            proxy_array = create_proxy_array(config["proxy_vm"])

        # Get a list of DRAFT blueprints
        payload = {"filter": "state==DRAFT"}
        draft_resp = body_via_v3_post(
            pc_external_ip, "blueprints", pc_password, payload
        ).json

        # Loop through the blueprints to modify
        for bp in draft_resp["entities"]:

            # Get the body of our blueprint
            bp_body = body_via_v3_get(
                pc_external_ip, "blueprints", pc_password, bp["metadata"]["uuid"]
            ).json

            # Remove unneeded status
            del bp_body["status"]

            # Configure secrets
            for secret in bp_body["spec"]["resources"]["credential_definition_list"]:
                secret["secret"]["attrs"]["is_secret_modified"] = True
                # Handle PE and PC Creds which are unique
                if secret["name"].lower() == "pc_creds":
                    secret["secret"]["username"] = "admin"
                    secret["secret"]["value"] = pc_password
                elif secret["name"].lower() == "pe_creds":
                    secret["secret"]["username"] = "admin"
                    secret["secret"]["value"] = pe_password
                # Find a matching type/username from our secret_spec
                else:
                    for ss in secret_spec["entities"]:
                        if (
                            secret["type"] == ss["type"]
                            and secret["username"] == ss["username"]
                        ):
                            secret["secret"]["value"] = ss["secret"]
                print(f"secret: {secret}")

            # Configure NICs and Images
            for substrate in bp_body["spec"]["resources"]["substrate_definition_list"]:
                if substrate["type"] == "AHV_VM":

                    # For NICs, determine if it's an infra or user VM based blueprint
                    for nic in substrate["create_spec"]["resources"]["nic_list"]:
                        if "infra" in bp_body["metadata"]["name"].lower():
                            # Ensure we have a proxy_vm config
                            if len(proxy_array) > 0:
                                nic["subnet_reference"]["uuid"] = infra_subnet_info[
                                    "uuid"
                                ]
                                nic["subnet_reference"]["name"] = infra_subnet_info[
                                    "name"
                                ]
                                proxy_ips = proxy_array.pop()
                                nic["ip_endpoint_list"][0]["ip"] = proxy_ips[1]
                            else:
                                print(
                                    f'Blueprint "{bp_body["metadata"]["name"]}" has '
                                    + f'"infra" in the name, but there were not enough '
                                    + f" proxy IPs configured: {config}. If"
                                    + f" this application needs external access, "
                                    + f"please ensure enough proxy IPs are in your GCP "
                                    + f'cluster.  Otherwise, remove "infra" from the '
                                    + f"blueprint name."
                                )
                        else:
                            nic["subnet_reference"]["uuid"] = subnet_info["uuid"]
                            nic["subnet_reference"]["name"] = subnet_info["name"]
                        print(json.dumps(nic, sort_keys=True, indent=4))

                    for disk in substrate["create_spec"]["resources"]["disk_list"]:
                        if (
                            disk["data_source_reference"] is not None
                            and disk["data_source_reference"]["kind"] == "image"
                        ):
                            for image in image_info["entities"]:
                                if (
                                    image["status"]["name"]
                                    == disk["data_source_reference"]["name"]
                                ):
                                    disk["data_source_reference"]["uuid"] = image[
                                        "metadata"
                                    ]["uuid"]
                                    print(json.dumps(disk, sort_keys=True, indent=4))

            # Update our blueprint
            resp = update_via_v3_put(
                pc_external_ip,
                "blueprints",
                pc_password,
                bp["metadata"]["uuid"],
                bp_body,
            )

            # Log appropriately based on response
            if resp.code == 200 or resp.code == 202:
                print(f"{bp['metadata']['name']} blueprint updated successfully.")
            else:
                raise Exception(
                    f"{bp['metadata']['name']} blueprint update failed with:\n"
                    + f"Resp: {resp}\n"
                    + f"Error Code: {resp.code}\n"
                    + f"Error Message: {resp.message}"
                )

    except Exception as ex:
        print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
