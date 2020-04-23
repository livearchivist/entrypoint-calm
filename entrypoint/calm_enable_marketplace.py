"""
calm_enable_marketplace.py: automation to enable the
Nutanix Marketplace on NX-on-GCP / Test Drive.

Author: michael@nutanix.com
Date:   2020-02-29
"""

import sys
import os
import json
import traceback

sys.path.append(os.path.join(os.getcwd(), "nutest_gcp.egg"))

from framework.lib.nulog import INFO, ERROR
from helpers.rest import RequestResponse
from helpers.calm import create_via_v3_post


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

        # Create the API call body
        body = {"enable_nutanix_apps": True}

        # Make API call to enable marketplace
        resp = create_via_v3_post(
            pc_external_ip, "marketplace_items/config", pc_password, body
        )

        # Log appropriately based on response
        if resp.code == 200 or resp.code == 202:
            INFO("Marketplace enabled successfully.")
        else:
            raise Exception(
                f"Marketplace enable failed with:\n"
                + f"Resp: {resp}\n"
                + f"Error Code: {resp.code}\n"
                + f"Error Message: {resp.message}"
            )

    except Exception as ex:
        ERROR(traceback.format_exc())


if __name__ == "__main__":
    main()

