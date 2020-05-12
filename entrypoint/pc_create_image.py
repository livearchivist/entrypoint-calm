"""
calm_create_image.py: automation to create a
CentOS 7 image on NX-on-GCP / Test Drive.

Author: michael@nutanix.com
Date:   2020-02-24
"""

import sys
import os
import json
import traceback

from helpers.rest import RequestResponse
from helpers.calm import (
    file_to_dict,
    create_via_v3_post,
    uuid_via_v3_post,
    body_via_v3_get,
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

        # Read in the spec file and conver to dict
        image_spec = file_to_dict("specs/pc_image.json")
        print(f"image_spec: {image_spec}")

        # Loop through each image
        for image in image_spec["entities"]:

            # Make API call to create image
            resp = create_via_v3_post(pc_external_ip, "images", pc_password, image)

            # Log appropriately based on response
            if resp.code == 200 or resp.code == 202:
                print(f"image['spec']['name'] Image created successfully.")
            else:
                raise Exception(
                    f"image['spec']['name'] Image create "
                    + f"failed with:\n"
                    + f"Error Code: {resp.code}\n"
                    + f"Error Message: {resp.message}"
                )

    except Exception as ex:
        print(traceback.format_exc())


if __name__ == "__main__":
    main()

