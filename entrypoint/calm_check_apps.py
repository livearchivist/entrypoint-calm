"""
calm_check_apps.py: automation to ensure that any launched
apps are in a RUNNING state.

Author: michael@nutanix.com
Date:   2020-04-21
"""

from helpers.calm import body_via_v3_post
from helpers.rest import RequestResponse
from framework.lib.nulog import INFO, ERROR
import sys
import os
import json
import time

sys.path.append(os.path.join(os.getcwd(), "nutest_gcp.egg"))


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

        # Get a list of apps
        apps = body_via_v3_post(pc_external_ip, "apps", pc_password, None).json

        # Loop through our apps
        for app in apps["entities"]:

            # Print out status
            INFO(f'{app["status"]["name"]} App State: {app["status"]["state"]}')

            # Fail out if app is not in running state
            if app["status"]["state"].lower() != "running":
                raise Exception(f"{app['status']['name']} app in a non-running state.")

    except Exception as ex:
        ERROR(ex)
        # NX-on-GCP does not support erroring out based on return codes,
        # so sleeping to time the deployment out
        time.sleep(18000)


if __name__ == "__main__":
    main()
