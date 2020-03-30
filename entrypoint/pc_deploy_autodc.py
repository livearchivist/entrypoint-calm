"""
deploy_autodc.py: automation to deploy
Alpine Linux Domain Controller on 
NX-on-GCP / Test Drive
Author: laura@nutanix.com
Date:   2020-03-13
"""

import sys
import os
import json
import time

sys.path.append(os.path.join(os.getcwd(), "nutest_gcp.egg"))

from framework.lib.nulog import INFO, ERROR
from framework.entities.image.image import Image
from framework.interfaces.interface import Interface
from framework.entities.cluster.nos_cluster import NOSCluster


# Given a filename, return a dict of the file's contents
def file_to_dict(filename):
  with open(os.path.join(os.getcwd(), filename)) as json_file:
    return json.load(json_file)


def create_vm(cluster, vm_name, image_name, network_name, assigned_ip):
  """
  :param vm_name: name of the VMs. wil be appended by 1,2,3,...
  :param image_name: name of the image the vms will be created with
  """
  cluster.execute('acli vm.create {vm_name}'.format(vm_name=vm_name))
  cluster.execute('acli vm.disk_create {vm_name}'
                  ' clone_from_image={image_name}'.
                  format(vm_name=vm_name, image_name=image_name))
  cluster.execute('acli vm.nic_create {vm_name}'
                  ' network={network} ip={ip}'.
                 format(vm_name=vm_name, network=network_name, ip=assigned_ip))
  cluster.execute('acli vm.on {vm_name}'.format(vm_name=vm_name))

def main():

  config = json.loads(os.environ["CUSTOM_SCRIPT_CONFIG"])
  INFO(config)

  cvm_info = config.get("tdaas_cluster")
  cvm_external_ip = cvm_info.get("ips")[0][0]
  cluster = NOSCluster(cluster=cvm_external_ip, configured=False)

  autodc_spec = file_to_dict("specs/pc_autodc.spec")
  subnet_spec = file_to_dict("specs/calm_subnet.spec")
  INFO("autodc_spec: " + str(autodc_spec))
  INFO("subnet_spec: " + str(subnet_spec))
  autodc_ip = autodc_spec["directoryUrl"].split("/")[2].split(":")[0]

  create_vm(cluster=cluster,
            vm_name='AutoDC2',
            image_name='AutoDC2.qcow2',
            network_name=subnet_spec["name"],
            assigned_ip=autodc_ip
            )

if __name__ == '__main__':
  main()
