'''
helpers/calm.py: Common functions to enable Calm API based
automation for NX-on-GCP.

Author: michael@nutanix.com
Date:   2020-02-24
'''

import sys
import os
import requests
import urllib3
import json

sys.path.append(os.path.join(os.getcwd(), "nutest_gcp.egg"))

from framework.lib.nulog import INFO, ERROR
from helpers.rest import (RequestParameters, RequestResponse,
                          RESTClient)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Given a filename, return a dict of the file's contents
def file_to_dict(filename):
  with open(os.path.join(os.getcwd(), filename)) as json_file:
    return json.load(json_file)


# Given an IP and Endpoint, return Nutanix v3 API URL
def create_v3_url(ip, endpoint):
  return f"https://{ip}:9440/api/nutanix/v3/{endpoint}"


# Create a new entity via a v3 post call, return the response
def create_via_v3_post(ip, endpoint, password, body):

  # Make the API call
  parameters = RequestParameters(
          uri=create_v3_url(ip, f"{endpoint}"),
          username="admin",
          password=password,
          method="post",
          payload=json.dumps(body),
          files=None
    )
  rest_client = RESTClient(parameters)
  resp = rest_client.request()
  INFO(f"create_via_v3_post: {ip}, {endpoint}")

  return resp  


# Uploads a named blueprint to a particular project
def upload_bp_via_v3_post(ip, password,
                          body, filename):

  # Create the file dictionary
  files = {
    "file": open(f"blueprints/{filename}", "rb")
  }

  # Make the API call
  parameters = RequestParameters(
          uri=create_v3_url(ip, "blueprints/import_file"),
          username="admin",
          password=password,
          method="post",
          payload=body,
          files=files
    )
  rest_client = RESTClient(parameters)
  resp = rest_client.request()
  INFO(f"upload_bp_via_v3_post: {ip}, {body}")

  return resp

# Uploads an app_icon
def upload_icon_via_v3_post(ip, password,
                            body, icon):

  # Create the file dictionary
  files = {
    "image": (icon["file"],
              open(f"images/{icon['name']}", "rb"),
              "image/png"
             )
  }

  # Make the API call
  parameters = RequestParameters(
          uri=create_v3_url(ip, "app_icons/upload"),
          username="admin",
          password=password,
          method="post",
          payload=body,
          files=files
    )
  rest_client = RESTClient(parameters)
  resp = rest_client.request()
  INFO(f"upload_icon_via_v3_post: {ip}, {body}")

  return resp



# Return the UUID of a desired entity.  If entity_name is empty
# assume a single entity in response and send first UUID
def uuid_via_v3_post(ip, endpoint, password, entity_name):

  # Make the API call
  parameters = RequestParameters(
          uri=create_v3_url(ip, f"{endpoint}/list"),
          username="admin",
          password=password,
          method="post",
          payload="{\"length\": 100}",
          files=None
    )
  rest_client = RESTClient(parameters)
  resp = rest_client.request()
  INFO(f"uuid_via_v3_post: {ip}, {endpoint}, {entity_name}")

  # Return UUID
  for entity in resp.json["entities"]:
    if entity_name == "":
      return entity["metadata"]["uuid"]
    elif entity["status"]["name"] == entity_name:
      return entity["metadata"]["uuid"]


# Return the body of a group of entities
# If payload is None, assume length=100
def body_via_v3_post(ip, endpoint, password, payload):

  # Determine payload
  if payload is None:
    payload = {
      "length": 100
    }

  # Make the API call
  parameters = RequestParameters(
          uri=create_v3_url(ip, f"{endpoint}/list"),
          username="admin",
          password=password,
          method="post",
          payload=json.dumps(payload),
          files=None
    )
  rest_client = RESTClient(parameters)
  resp = rest_client.request()
  INFO(f"body_via_v3_post: {ip}, {endpoint}")

  # Return the response
  return resp


# Return the body of a desired entity
def body_via_v3_get(ip, endpoint, password, entity_uuid):

  # Make the API call
  parameters = RequestParameters(
        uri=create_v3_url(ip, f"{endpoint}/{entity_uuid}"),
        username="admin",
        password=password,
        method="get",
        payload=None,
        files=None
  )
  rest_client = RESTClient(parameters)
  resp = rest_client.request()
  INFO(f"body_via_v3_get: {ip}, {endpoint}, {entity_uuid}")

  # Return the response
  return resp


# Update a given entity with a PUT
def update_via_v3_put(ip, endpoint, password, entity_uuid,
                      body):

  # Make the API call
  parameters = RequestParameters(
        uri=create_v3_url(ip, f"{endpoint}/{entity_uuid}"),
        username="admin",
        password=password,
        method="put",
        payload=json.dumps(body),
        files=None
  )
  rest_client = RESTClient(parameters)
  resp = rest_client.request()
  INFO(f"update_via_v3_put: {ip}, {endpoint}, {entity_uuid}")

  # Return the response
  return resp


# Given a VLAN ID, return a dict of the matching
# Subnet UUID and name
def get_subnet_info(ip, password, vlan_id):

  subnet_info = {}

  # Get our subnet info from the infra
  subnets_body = body_via_v3_post(ip, "subnets", password,
                                  None)
  for subnet in subnets_body.json["entities"]:
    if subnet["spec"]["resources"]["vlan_id"] == vlan_id:
      subnet_info["name"] = subnet["spec"]["name"]
      subnet_info["uuid"] = subnet["metadata"]["uuid"]

  return subnet_info

