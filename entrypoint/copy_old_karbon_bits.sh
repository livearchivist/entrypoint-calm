#!/bin/bash
set -ex

# Get PC IP, and strip suffix and prefix "
PC_IP=$(jq '.tdaas_pc.ips[0][0]' /home/config.json)
PC_IP="${PC_IP%\"}"
PC_IP="${PC_IP#\"}"
echo $PC_IP

# Add PC Key to known_hosts
ssh-keyscan $PC_IP | grep nistp521 > /root/.ssh/known_hosts

# Copy over the older containers
ssh nutanix@$PC_IP 'sudo wget -O /home/docker/karbon_core/karbon-core.tar.xz https://storage.googleapis.com/testdrive-templates/library/release/karbon/karbon-core.tar.xz.old'
ssh nutanix@$PC_IP 'sudo wget -O /home/docker/karbon_ui/karbon-ui.tar.xz https://storage.googleapis.com/testdrive-templates/library/release/karbon/karbon-ui.tar.xz.old'
