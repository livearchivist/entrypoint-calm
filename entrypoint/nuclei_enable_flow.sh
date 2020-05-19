#!/bin/bash
set -ex

# Get PC IP, and strip suffix and prefix "
PC_IP=$(jq '.tdaas_pc.ips[0][0]' /home/config.json)
PC_IP="${PC_IP%\"}"
PC_IP="${PC_IP#\"}"
echo $PC_IP

# Do the same for the PC Password
PC_PASS=$(jq '.tdaas_pc.prism_password' /home/config.json)
PC_PASS="${PC_PASS%\"}"
PC_PASS="${PC_PASS#\"}"
echo $PC_PASS

# Add PC Key to known_hosts
ssh-keyscan $PC_IP | grep nistp521 > /root/.ssh/known_hosts

# Enable Flow
<&- ssh nutanix@$PC_IP "bash -lc 'nuclei -server localhost -username admin -password $PC_PASS microseg.enable'"
