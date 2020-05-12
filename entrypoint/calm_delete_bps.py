"""
calm_delete_apps.py: automation to delete
Nutanix Calm blueprints.

Author: michael@nutanix.com
Date:   2020-04-25
"""

import sys
import os
import json
import time
import traceback

from helpers.rest import RequestResponse
from helpers.calm import uuid_via_v3_post, file_to_dict, del_via_v3_delete


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

        # Read in the delete spec file
        delete_spec = file_to_dict("specs/calm_bp_delete.json")

        # Loop through the bps to delete
        for bp in delete_spec["entities"]:

            # Get the bp uuid
            bp_uuid = uuid_via_v3_post(
                pc_external_ip, "blueprints", pc_password, bp["bp_name"]
            )

            # Delete the bp
            resp = del_via_v3_delete(pc_external_ip, "blueprints", pc_password, bp_uuid)

            # Log appropriately based on response
            if resp.code == 200 or resp.code == 202:
                print(f'{bp["bp_name"]} blueprint deleted successfully.')
            else:
                raise Exception(
                    'f{bp["bp_name"]} blueprint delete failed with:\n'
                    + f"Resp: {resp}\n"
                    + f"Error Code: {resp.code}\n"
                    + f"Error Message: {resp.message}"
                )

    except Exception as ex:
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
