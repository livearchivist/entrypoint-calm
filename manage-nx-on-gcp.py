#!/usr/local/bin/python3
"""
deploy-nx-on-gcp.py: automation to manage NX-on-GCP Test Drive
clusters.  All functions are included within this file so it's
easily distributable.

Instructions:
1. Add the following GCP Service Account into your GCP Project via
   the IAM section, with "Project Editor" permissions.
   69118586847-compute@developer.gserviceaccount.com
2. Find the "MODIFY FOR YOUR ENVIRONMENT" section below, and
   replace the values with your project details.
3. Run the following command to get help outputs on the various
   ways to run the script.
   python3 manage-nx-on-gcp.py help

Author: michael@nutanix.com
Date:   2020-03-12
"""

import sys
import os
import json
import requests
import time


# Given a filename, return a dict of the file's contents
def file_to_dict(filename):
  with open(os.path.join(os.getcwd(), filename)) as json_file:
    return json.load(json_file)


# ================== MODIFY FOR YOUR ENVIRONMENT ==================
metadata = {          
  "projects": ["nutanix-expo"], # replace with your project name
  "duration": 1, # replace with your desired number of hours
  "name": time.strftime("%Y-%m-%d %H:%M:%S") # optionally change
}

service_name = file_to_dict("service_name.json")["name"]
# Store the name of your service in a file titled service_name.json
# It should be a json with a single key "name", and the value will
# be the name of the service given by the NX-on-GCP ENG team.
# This file must be added to your .gitignore, as its contents
# should not be on public GitHub repos.
# =================================================================


# Function to print script usage help
def print_help():
  print("To deploy a cluster, specify a json template file:")
  print("  python3 manage-nx-on-gcp.py path/to/cluster-spec.json\n")
  print("To get cluster deployment info, specify the request_id " +
        "UUID and append .info:")
  print("  python3 manage-nx-on-gcp.py <request_id-uuid>.info\n")
  print("To modify a cluster's duration, specify the request_id " +
        "UUID and append .mod:")
  print("  python3 manage-nx-on-gcp.py <request_id-uuid>.mod\n")
  print("To get cluster deployment logs, specify the request_id " +
        "UUID and append .logs:")
  print("  python3 manage-nx-on-gcp.py <request_id-uuid>.logs\n")
  print("To delete a cluster, specify the request_id " +
        "UUID and append .del:")
  print("  python3 manage-nx-on-gcp.py <request_id-uuid>.del\n")


# Output the cluster info
def info(cluster):

  # Create the headers
  headers = {
    "request-type": "SERVICE",
    "request-service-name": service_name
  }

  # Create the URL and make the call
  req_id = cluster.strip(".info")
  url = f"https://nx-gcp.nutanix.com/api/v1/deployments/requests/{req_id}"
  resp = requests.get(url, headers=headers)

  # Handle success or failure
  if resp.ok:
    cluster_info = json.loads(resp.content.decode("utf-8"))
    print(json.dumps(cluster_info, indent=4, sort_keys=True))

  else:
    print("Request failed with the following detail:")
    print(str(resp))


# Create a cluster for a specified file
def create(cluster):

  # Read in the spec file and conver to dict
  cluster_spec = file_to_dict(cluster)

  # Create the headers
  headers = {
    "request-type": "SERVICE",
    "request-service-name": service_name
  }

  # Create the payload
  payload = {
    "resource_specs": cluster_spec,
    "metadata": metadata
  }

  # Create the URL and make the call
  url = "https://nx-gcp.nutanix.com/api/v1/deployments/requests"
  resp = requests.post(url, json=payload, headers=headers)

  # Handle success
  if resp.ok:

    # Set the response as a dictionary (return is a byte)
    request_info = json.loads(resp.content.decode("utf-8"))
    print(request_info["message"])
    print(f"request_id: {request_info['data']['request_id']}")

    # Add the request id to the file for usage later
    f = open("requests.ids", "a")
    f.write(f"{metadata['name']}:    {request_info['data']['request_id']}\n")
    f.close()
    print("The request_id has been added to your 'requests.ids' file.\n")

    # Call the info function to get additional detail on the deployment
    time.sleep(5)
    info(request_info['data']['request_id'])

  # Handle failure
  else:
    print("Request failed with the following detail:")
    print(json.dumps(json.loads(resp.content.decode("utf-8")),
          indent=4, sort_keys=True))


# Main function, handle inputs and call correct functions
if __name__ == '__main__':

  # Error out if no spec file was passed via CLI
  if len(sys.argv) == 1:
    print("Error: please specify at least one argument when running " +
          "this script.  Examples:\n")
    print_help()

  # Print script info if "help" is passed
  elif sys.argv[1].lower().endswith("help") or\
       sys.argv[1].lower() == "-h":
    print("Use this script to deploy, manage, and reclaim NX-on-GCP " +
          "clusters.\n")
    print_help()

  # Create an NX-on-GCP cluster for each cluster spec file
  else:
    for cluster in sys.argv:
      if not cluster.endswith("py"):
        # Create a cluster
        if cluster.endswith("json"):
          create(cluster)
        # Get info on a cluster
        elif cluster.endswith("info"):
          info(cluster)
        # Download logs for a cluster
        elif cluster.endswith("logs"):
          logs(cluster)
        # Extend a cluster's duration
        elif cluster.endswith("mod"):
          modify(cluster)
        # Delete a cluster
        elif cluster.endswith("del"):
          delete(cluster)
        else:
          print("Error: you did not specify a valid argument.\n")
          print_help()

