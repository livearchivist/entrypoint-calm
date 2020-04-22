"""
calm_approve_bp.py: automation to approve blueprints in
the Marketplace Manager on NX-on-GCP / Test Drive.

Author: michael@nutanix.com
Date:   2020-03-18
"""

import sys
import os
import json
import uuid
import traceback

sys.path.append(os.path.join(os.getcwd(), "nutest_gcp.egg"))

from framework.lib.nulog import INFO, ERROR
from helpers.rest import RequestResponse
from helpers.calm import (
    file_to_dict,
    body_via_v3_get,
    body_via_v3_post,
    update_via_v3_put,
)


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

        # Get marketplace items
        mp_items = body_via_v3_post(
            pc_external_ip, "calm_marketplace_items", pc_password, None
        ).json

        # Loop through our items
        for item in mp_items["entities"]:

            # We only care about those PENDING
            if item["status"]["app_state"] == "PENDING":

                # Get and modify the body
                body = body_via_v3_get(
                    pc_external_ip,
                    "calm_marketplace_items",
                    pc_password,
                    item["metadata"]["uuid"],
                ).json
                del body["status"]
                body["spec"]["resources"]["app_state"] = "ACCEPTED"

                # Update the item
                resp = update_via_v3_put(
                    pc_external_ip,
                    "calm_marketplace_items",
                    pc_password,
                    item["metadata"]["uuid"],
                    body,
                )

                # Log appropriately based on response
                if resp.code == 200 or resp.code == 202:
                    INFO(f"{item['status']['name']} bp approved successfully.")
                else:
                    raise Exception(
                        f"{item['status']['name']} bp approved"
                        + f" failed with:\n"
                        + f"Error Code: {resp.code}\n"
                        + f"Error Message: {resp.message}"
                    )

    except Exception as ex:
        ERROR(traceback.format_exc())


if __name__ == "__main__":
    main()
