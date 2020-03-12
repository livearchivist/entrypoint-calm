"""
deploy-nx-on-gcp.py: automation to deploy an NX-on-GCP Test Drive
cluster.  All functions are included within this file so it's
easily distributable.

Instructions:
1. Add the following GCP Service Account into your GCP Project via
   the IAM section, with "Project Editor" permissions.
   69118586847-compute@developer.gserviceaccount.com
2. Find the "MODIFY FOR YOUR ENVIRONMENT" section below, and
   replace the values with your project details.
3. Run the script with the following syntax, substituting in your
   specific json file(s), either relative or absolute path
   python3 deploy-nx-on-gcp.py path/to/cluster-spec.json

Author: michael@nutanix.com
Date:   2020-03-12
"""

import sys
import os
import json
import requests
import time

# ================== MODIFY FOR YOUR ENVIRONMENT ==================
metadata = {          
  "projects": ["nutanix-expo"], # replace with your project name
  "duration": 1, # replace with your desired number of hours
  "name": time.strftime("%Y%m%d%H%M%S") # optionally change
}

service_name = "$TESTDRIVE" # At the time of this script's writing,
# "$TESTDRIVE" is the only supported value by the NX-on-GCP team.
# However, in the future the supported values will be increased as
# they add additional templates.
# =================================================================


# Given a filename, return a dict of the file's contents
def file_to_dict(filename):
  with open(os.path.join(os.getcwd(), filename)) as json_file:
    return json.load(json_file)

# Create a cluster for each specified file
def main(cluster):

  # Read in the spec files and conver to dicts
  cluster_spec = file_to_dict(cluster)
  print(f"cluster_spec: {cluster_spec}")

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
  url = 'https://nx-gcp.nutanix.com/api/v1/deployments/requests'
  resp = requests.post(url, json=payload, headers=headers)

  # Handle success or failure
  if resp.ok:
    print(f"Request successfully submitted: {metadata['name']}")
    print(json.dumps(resp.content, indent=4))

  else:
    print("Request failed with the following detail:")
    print(json.dumps(resp.content, indent=4))
    

if __name__ == '__main__':

  # Error out if no spec file was passed via CLI
  if len(sys.argv) == 1:
    print("Error: please specify a spec file when running this script.")
    print("python3 deploy-nx-on-gcp.py path/to/cluster-spec.json")

  # Create an NX-on-GCP cluster for each cluster spec file
  else:
    for cluster in sys.argv:
      if not cluster.endswith("py"):
        main(cluster)

