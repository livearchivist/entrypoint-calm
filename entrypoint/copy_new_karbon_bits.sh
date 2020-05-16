#!/bin/bash
set -ex

# Get PC IP, and strip suffix and prefix "
PC_IP=$(jq '.tdaas_pc.ips[0][0]' /home/config.json)
PC_IP="${PC_IP%\"}"
PC_IP="${PC_IP#\"}"
echo $PC_IP

# Stop karbon_core and karbon_ui services
ssh nutanix@$PC_IP 'source /etc/profile; genesis stop karbon_core karbon_ui'

# Remove the old containers
ssh nutanix@$PC_IP "docker image rm \$(docker image ls | grep karbon-core | awk '{print \$3}')"
ssh nutanix@$PC_IP "docker image rm \$(docker image ls | grep karbon-ui | awk '{print \$3}')"

# Copy over the containers
ssh nutanix@$PC_IP 'sudo wget -O /home/docker/karbon_core/karbon-core.tar.xz https://storage.googleapis.com/testdrive-templates/library/release/karbon/karbon-core.tar.xz'
ssh nutanix@$PC_IP 'sudo wget -O /home/docker/karbon_ui/karbon-ui.tar.xz https://storage.googleapis.com/testdrive-templates/library/release/karbon/karbon-ui.tar.xz'

# Start the services back up
ssh nutanix@$PC_IP 'source /etc/profile; cluster start'
