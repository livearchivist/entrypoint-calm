"""
pc_ssh_keys.py: automation to configure PC with an SSH Key
for passwordless SSH on NX-on-GCP / Test Drive.

Author: michael@nutanix.com
Date:   2020-04-16
"""

import sys
import os
import json
import traceback

sys.path.append(os.path.join(os.getcwd(), "nutest_gcp.egg"))

from framework.lib.nulog import INFO, ERROR
from helpers.rest import RequestResponse
from helpers.calm import file_to_string, create_via_v1_post


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

        # Read in our public key and create our payload
        public_key = file_to_string("/root/.ssh/id_rsa.pub")
        INFO(f"public_key: {public_key}")
        payload = {"name": "plugin-runner", "key": public_key}

        # Make API call to configure the authconfig
        resp = create_via_v1_post(
            pc_external_ip, "cluster/public_keys", pc_password, payload,
        )

        # Log appropriately based on response
        if resp.code == 200 or resp.code == 202:
            INFO("SSH Key added to PC successfully.")
        else:
            raise Exception(
                f"SSH Key failed to add to PC with:\n"
                + f"Resp: {resp}\n"
                + f"Error Code: {resp.code}\n"
                + f"Error Message: {resp.message}"
            )

    except Exception as ex:
        ERROR(traceback.format_exc())


if __name__ == "__main__":
    main()

