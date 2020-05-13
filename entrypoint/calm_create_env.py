"""
calm_create_env.py: automation to create a
Calm environment on NX-on-GCP / Test Drive.

Author: michael@nutanix.com
Date:   2020-02-24
"""

import sys
import os
import json
import uuid
import traceback

from helpers.calm import (
    file_to_dict,
    uuid_via_v3_post,
    create_via_v3_post,
    get_subnet_info,
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

        # Read in the spec files and convert to dicts
        env_spec = file_to_dict("specs/calm_environment.json")
        image_spec = file_to_dict("specs/pc_image.json")
        subnet_spec = file_to_dict("specs/calm_subnet.json")
        secret_spec = file_to_dict("specs/calm_secrets.json")

        # Get our subnet info from the infra
        subnet_info = get_subnet_info(
            pc_external_ip, pc_password, subnet_spec["entities"][0]["vlan"]
        )
        print(f"subnet_uuid: {subnet_info['uuid']}")

        # Get our image info from the infra
        cent_image_name = image_spec["entities"][0]["metadata"]["name"]
        cent_image_uuid = uuid_via_v3_post(
            pc_external_ip, "images", pc_password, cent_image_name
        )
        print(f"cent_image_uuid: {cent_image_uuid}")
        # win_image_name = image_spec["entities"][1]["metadata"]["name"]
        # win_image_uuid = uuid_via_v3_post(pc_external_ip, "images",
        #                                   pc_password, win_image_name)
        # print(f"win_image_uuid: {win_image_uuid}")

        # Generate UUIDs for new components
        env_name = str(uuid.uuid4())
        env_uuid = str(uuid.uuid4())
        cent_substrate_uuid = str(uuid.uuid4())
        # win_substrate_uuid = str(uuid.uuid4())
        cent_key_uuid = str(uuid.uuid4())
        cent_pass_uuid = str(uuid.uuid4())
        # win_pass_uuid = str(uuid.uuid4())

        # Sub in our UUIDs and names:
        # env
        env_spec["spec"]["name"] = env_name
        env_spec["metadata"]["name"] = env_name
        env_spec["metadata"]["uuid"] = env_uuid

        # substrate
        env_spec["spec"]["resources"]["substrate_definition_list"][0][
            "uuid"
        ] = cent_substrate_uuid
        # env_spec["spec"]["resources"]["substrate_definition_list"][1]\
        #        ["uuid"] = win_substrate_uuid

        # account
        env_spec["spec"]["resources"]["substrate_definition_list"][0][
            "readiness_probe"
        ]["login_credential_local_reference"]["uuid"] = cent_key_uuid
        # env_spec["spec"]["resources"]["substrate_definition_list"][1]\
        #        ["readiness_probe"]["login_credential_local_reference"]\
        #        ["uuid"] = win_pass_uuid

        # subnet
        env_spec["spec"]["resources"]["substrate_definition_list"][0]["create_spec"][
            "resources"
        ]["nic_list"][0]["subnet_reference"]["uuid"] = subnet_info["uuid"]
        # env_spec["spec"]["resources"]["substrate_definition_list"][1]\
        #        ["create_spec"]["resources"]["nic_list"][0]\
        #        ["subnet_reference"]["uuid"] = subnet_info["uuid"]

        # image
        env_spec["spec"]["resources"]["substrate_definition_list"][0]["create_spec"][
            "resources"
        ]["disk_list"][0]["data_source_reference"]["name"] = cent_image_name
        env_spec["spec"]["resources"]["substrate_definition_list"][0]["create_spec"][
            "resources"
        ]["disk_list"][0]["data_source_reference"]["uuid"] = cent_image_uuid
        # env_spec["spec"]["resources"]["substrate_definition_list"][1]\
        #        ["create_spec"]["resources"]["disk_list"][0]\
        #        ["data_source_reference"]["name"] = win_image_name
        # env_spec["spec"]["resources"]["substrate_definition_list"][1]\
        #        ["create_spec"]["resources"]["disk_list"][0]\
        #        ["data_source_reference"]["uuid"] = win_image_uuid

        # secrets
        for secret in secret_spec["entities"]:
            if secret["name"] == "CENTOS_KEY":
                suuid = cent_key_uuid
            elif secret["name"] == "CENTOS_PASS":
                suuid = cent_pass_uuid
            else:
                continue
            env_spec["spec"]["resources"]["credential_definition_list"].append(
                {
                    "name": secret["name"],
                    "type": secret["type"],
                    "username": secret["username"],
                    "secret": {
                        "attrs": {"is_secret_modified": True},
                        "value": secret["secret"],
                    },
                    "uuid": suuid,
                }
            )

        # Make the API call to create the environment
        print(f"env_spec: {env_spec}")
        resp = create_via_v3_post(pc_external_ip, "environments", pc_password, env_spec)

        # Log appropriately based on response
        if resp.code == 200 or resp.code == 202:
            print(f"{env_spec['spec']['name']} Env created successfully.")
        else:
            raise Exception(
                f"{env_spec['spec']['name']} Env create failed with:\n"
                + f"Resp: {resp}\n"
                + f"Error Code: {resp.code}\n"
                + f"Error Message: {resp.message}"
            )

    except Exception as ex:
        print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()

