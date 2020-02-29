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

sys.path.append(os.path.join(os.getcwd(), "nutest_gcp.egg"))

from framework.lib.nulog import INFO, ERROR
from helpers.calm import (file_to_dict, uuid_via_v3_post,
                          body_via_v3_get, body_via_v3_post)


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

    # Read in the spec files and convert to dicts
    env_spec = file_to_dict("calm_environment.spec")
    pass_spec = file_to_dict("calm_userpassword.spec")
    key_spec = file_to_dict("calm_userkey.spec")

    # Logic due to the fake Prism Pro Account
    accounts_resp = body_via_v3_post(pc_external_ip, "accounts",
                                     pc_password)
    for account in accounts_resp.json["entities"]:
      if account["status"]["resources"]["state"] == "VERIFIED":
        account_uuid = account["metadata"]["uuid"]    
    INFO(f"account_uuid: {account_uuid}")

    # Get our subnet info from the infra
    subnets_body = body_via_v3_post(pc_external_ip, "subnets",
                                    pc_password)
    for subnet in subnets_body.json["entities"]:
      if subnet["spec"]["resources"]["vlan_id"] == 1:
        subnet_name = subnet["spec"]["name"]
        subnet_uuid = subnet["metadata"]["uuid"]
    INFO(f"subnet_uuid: {subnet_uuid}")

    # Get our image info from the infra
    image_spec = file_to_dict("calm_image.spec")
    image_name = image_spec["metadata"]["name"]
    image_uuid = uuid_via_v3_post(pc_external_ip, "images",
                                  pc_password, image_name)
    INFO(f"image_uuid: {image_uuid}")
        
    # Generate UUIDs for new components
    env_name = uuid.uuid4()
    env_uuid = uuid.uuid4()
    substrate_uuid = uuid.uuid4()
    key_uuid = uuid.uuid4()
    pass_uuid = uuid.uuid4()

    # Sub in our UUIDs and names:
    # env
    env_spec["spec"]["name"] = env_name
    env_spec["metadata"]["name"] = env_name
    env_spec["metadata"]["uuid"] = env_uuid

    # substrate
    env_spec["spec"]["resources"]["substrate_definition_list"][0]\
            ["uuid"] = substrate_uuid

    # account
    env_spec["spec"]["resources"]["substrate_definition_list"][0]\
            ["readiness_probe"]["login_credential_local_reference"]\
            ["uuid"] = account_uuid

    # subnet
    env_spec["spec"]["resources"]["substrate_definition_list"][0]\
            ["create_spec"]["resources"]["nic_list"][0]\
            ["uuid"] = subnet_uuid

    # image
    env_spec["spec"]["resources"]["substrate_definition_list"][0]\
            ["create_spec"]["resources"]["disk_list"][0]\
            ["data_source_reference"]["name"] = image_name
    env_spec["spec"]["resources"]["substrate_definition_list"][0]\
            ["create_spec"]["resources"]["disk_list"][0]\
            ["data_source_reference"]["uuid"] = image_uuid

    # password credential
    env_spec["spec"]["resources"]["credential_definition_list"][0]\
            ["name"] = pass_spec["name"]
    env_spec["spec"]["resources"]["credential_definition_list"][0]\
            ["username"] = pass_spec["username"]
    env_spec["spec"]["resources"]["credential_definition_list"][0]\
            ["secret"]["value"] = pass_spec["secret"]
    env_spec["spec"]["resources"]["credential_definition_list"][0]\
            ["uuid"] = pass_uuid

    # key credential
    env_spec["spec"]["resources"]["credential_definition_list"][0]\
            ["name"] = key_spec["name"]
    env_spec["spec"]["resources"]["credential_definition_list"][0]\
            ["username"] = key_spec["username"]
    env_spec["spec"]["resources"]["credential_definition_list"][0]\
            ["secret"]["value"] = key_spec["secret"]
    env_spec["spec"]["resources"]["credential_definition_list"][0]\
            ["uuid"] = key_uuid

    # Make the API call to create the environment
    resp = create_via_v3_post(pc_external_ip, "environments",
                              pc_password, env_spec)

    # Log appropriately based on response
    if resp.code == 202:
      INFO(f"{env_spec['spec']['name']} Env created successfully.")
    else:
      raise Exception(f"{env_spec['spec']['name']} Env create" +
                      f" failed with:\n" +
                      f"Error Code: {resp.code}\n" +
                      f"Error Message: {resp.message}")

  except Exception as ex:
    INFO(ex)

if __name__ == '__main__':
  main()
