"""
pe_ntp.py: automation to add Users to PE
on NX-on-GCP / Test Drive.

Author: michael@nutanix.com
Date:   2020-05-11
"""

import sys
import os
import json
import traceback

from helpers.rest import RequestResponse
from helpers.calm import file_to_dict, create_via_v1_post, update_via_v1_put


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
        user_spec = file_to_dict("specs/pe_users.json")
        print(f"user_spec: {user_spec}")

        # Loop through our users
        for user in user_spec["entities"]:

            # Make API call to configure the authconfig
            resp = create_via_v1_post(pe_external_ip, "users", pe_password, user,)

            # If the add was successful, update the user
            if resp.code == 200 or resp.code == 202:
                print(f"PE user {user['profile']['username']} added successfully.")

                # Now make the user a non-viewer
                resp = update_via_v1_put(
                    pe_external_ip,
                    "users",
                    pe_password,
                    "karbon//roles",
                    user["roles"],
                )

                # Log appropriately based on response
                if resp.code == 200 or resp.code == 202:
                    print(
                        f"PE user {user['profile']['username']} updated successfully."
                    )
                else:
                    raise Exception(
                        f"PE user {user['profile']['username']} update failed with:\n"
                        + f"Resp: {resp}\n"
                        + f"Error Code: {resp.code}\n"
                        + f"Error Message: {resp.message}"
                    )
            else:
                raise Exception(
                    f"PE user {user['profile']['username']} add failed with:\n"
                    + f"Resp: {resp}\n"
                    + f"Error Code: {resp.code}\n"
                    + f"Error Message: {resp.message}"
                )

    except Exception as ex:
        print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()

