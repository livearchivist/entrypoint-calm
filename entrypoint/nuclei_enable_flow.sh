#!/bin/bash
set -ex

# Get PC IP, and strip suffix and prefix "
PC_IP=$(jq '.tdaas_pc.ips[0][0]' /home/config.json)
PC_IP="${PC_IP%\"}"
PC_IP="${PC_IP#\"}"
echo $PC_IP

# Add PC Key to known_hosts
ssh-keyscan $PC_IP | grep nistp521 > /root/.ssh/known_hosts

# Enable Flow
ssh -t nutanix@$PC_IP "bash -lc 'nuclei microseg.enable'"
