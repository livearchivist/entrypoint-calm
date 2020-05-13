"""
calm_upload_icons.py: automation to upload
blueprint icons on NX-on-GCP / Test Drive.

Author: michael@nutanix.com
Date:   2020-03-17
"""

import sys
import os
import json
import traceback

from helpers.rest import RequestResponse
from helpers.calm import file_to_dict, uuid_via_v3_post, upload_icon_via_v3_post


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

        # Read in the spec files and conver to dicts
        icon_spec = file_to_dict("specs/calm_icon.json")
        print(f"icon_spec: {icon_spec}")

        # Loop through the blueprints to upload
        for icon in icon_spec["entities"]:

            # Create our payload
            payload = {"name": icon["name"]}

            # Upload our icon
            resp = upload_icon_via_v3_post(pc_external_ip, pc_password, payload, icon)

            # Log appropriately based on response
            if resp.code == 200 or resp.code == 202:
                print(f"{icon['name']} icon created successfully.")
            else:
                raise Exception(
                    f"{icon['name']} icon create"
                    + f" failed with:\n"
                    + f"Error Code: {resp.code}\n"
                    + f"Error Message: {resp.message}"
                )

    except Exception as ex:
        print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()

