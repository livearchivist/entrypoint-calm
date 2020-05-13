"""
pe_ntp.py: automation to configure PE NTP
on NX-on-GCP / Test Drive.

Author: michael@nutanix.com
Date:   2020-03-30
"""

import sys
import os
import json
import traceback

from helpers.rest import RequestResponse
from helpers.calm import file_to_dict, create_via_v1_post


def main():

    # Get and log the config from the Env variable
    config = json.loads(os.environ["CUSTOM_SCRIPT_CONFIG"])
    print(config)

    # Get PE info from the config dict
    pe_info = config.get("tdaas_cluster")
    pe_external_ip = pe_info.get("ips")[0][0]
    pe_internal_ip = pe_info.get("ips")[0][1]
    pe_password = pe_info.get("prism_password")

    try:

        # Read in our spec file
        ntp_spec = file_to_dict("specs/ntp.json")
        print(f"ntp_spec: {ntp_spec}")

        # Make API call to configure the authconfig
        resp = create_via_v1_post(
            pe_external_ip,
            "cluster/ntp_servers/add_list",
            pe_password,
            ntp_spec["entities"],
        )

        # Log appropriately based on response
        if resp.code == 200 or resp.code == 202:
            print("PE NTP configured successfully.")
        else:
            raise Exception(
                f"PE NTP config failed with:\n"
                + f"Resp: {resp}\n"
                + f"Error Code: {resp.code}\n"
                + f"Error Message: {resp.message}"
            )

    except Exception as ex:
        print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()

