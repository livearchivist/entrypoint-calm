"""
calm_delete_apps.py: automation to delete or soft delete
Nutanix Calm applications.

Author: michael@nutanix.com
Date:   2020-04-25
"""

import sys
import os
import json
import time
import traceback

sys.path.append(os.path.join(os.getcwd(), "nutest_gcp.egg"))

from framework.lib.nulog import INFO, ERROR
from helpers.rest import RequestResponse
from helpers.calm import uuid_via_v3_post, file_to_dict, del_via_v3_delete


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

        # Read in the delete spec file
        delete_spec = file_to_dict("specs/calm_app_delete.json")

        # Loop through the apps to delete
        for app in delete_spec["entities"]:

            # Get the app uuid
            app_uuid = uuid_via_v3_post(
                pc_external_ip, "apps", pc_password, app["app_name"]
            )

            # Handle soft_delete
            if app["soft_delete"]:
                app_uuid = app_uuid + "?type=soft"

            # Delete the app
            resp = del_via_v3_delete(pc_external_ip, "apps", pc_password, app_uuid)

            # Log appropriately based on response
            if resp.code == 200 or resp.code == 202:
                INFO(f'{app["app_name"]} app deleted successfully.')
            else:
                raise Exception(
                    'f{app["app_name"]} app delete failed with:\n'
                    + +f"Resp: {resp}\n"
                    + f"Error Code: {resp.code}\n"
                    + f"Error Message: {resp.message}"
                )

    except Exception as ex:
        ERROR(traceback.format_exc())


if __name__ == "__main__":
    main()
