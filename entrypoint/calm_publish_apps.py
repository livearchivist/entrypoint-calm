"""
calm_publish_apps.py: automation to publish Nutanix
Marketplace apps on NX-on-GCP / Test Drive.

Author: michael@nutanix.com
Date:   2020-03-01
"""

import sys
import os
import json
import traceback

from helpers.calm import (
    body_via_v3_get,
    body_via_v3_post,
    update_via_v3_put,
    file_to_dict,
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

        # Convert our spec to dict
        apps_spec = file_to_dict("specs/calm_bp_publish.spec")

        # Get our non-default projects before the loop
        projects_payload = {"filter": "name!=default"}
        projects_resp = body_via_v3_post(
            pc_external_ip, "projects", pc_password, projects_payload
        )

        # Loop through our to-be-published apps
        for app in apps_spec["entities"]:

            # Construct payload and make call
            mp_payload = {"filter": f"name=={app['mp_name']}"}
            mp_post = body_via_v3_post(
                pc_external_ip, "calm_marketplace_items", pc_password, mp_payload
            )

            # Loop through our response to find matching version
            for mp_item in mp_post.json["entities"]:
                if (
                    mp_item["status"]["app_state"] == "ACCEPTED"
                    and mp_item["status"]["version"] == app["bp_version"]
                    and mp_item["status"]["app_source"] == app["app_source"]
                ):

                    # Make a GET with our UUID
                    mp_get = body_via_v3_get(
                        pc_external_ip,
                        "calm_marketplace_items",
                        pc_password,
                        mp_item["metadata"]["uuid"],
                    )

                    # Modify the response body
                    mp_body = mp_get.json
                    del mp_body["status"]
                    mp_body["spec"]["resources"]["app_state"] = "PUBLISHED"
                    for project in projects_resp.json["entities"]:
                        mp_body["spec"]["resources"]["project_reference_list"].append(
                            project["metadata"]["project_reference"]
                        )

                    # Publish the blueprint
                    pub_resp = update_via_v3_put(
                        pc_external_ip,
                        "calm_marketplace_items",
                        pc_password,
                        mp_body["metadata"]["uuid"],
                        mp_body,
                    )

                    # Log appropriately based on response
                    if pub_resp.code == 200 or pub_resp.code == 202:
                        print(
                            f"{mp_body['spec']['name']} MP item published successfully."
                        )
                    else:
                        raise Exception(
                            f"{mp_body['spec']['name']} MP App Publish"
                            + f" failed with:\n"
                            + f"Error Code: {pub_resp.code}\n"
                            + f"Error Message: {pub_resp.message}"
                        )

    except Exception as ex:
        print(traceback.format_exc())


if __name__ == "__main__":
    main()

