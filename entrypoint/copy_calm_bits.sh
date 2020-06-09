#!/bin/bash
set -ex

# Get PC IP, and strip suffix and prefix "
PC_IP=$(jq '.tdaas_pc.ips[0][0]' /home/config.json)
PC_IP="${PC_IP%\"}"
PC_IP="${PC_IP#\"}"
echo $PC_IP

# Add PC Key to known_hosts
ssh-keyscan $PC_IP | grep nistp521 > /root/.ssh/known_hosts

# Stop nucalm and epsilon services
ssh nutanix@$PC_IP 'source /etc/profile; genesis stop nucalm epsilon'
sleep 30

# Copy over the containers
ssh nutanix@$PC_IP 'sudo wget -O /usr/local/nutanix/nucalm/nucalm.tar.gz https://storage.googleapis.com/testdrive-templates/library/release/calm/nucalm.tar.gz'
ssh nutanix@$PC_IP 'sudo wget -O /usr/local/nutanix/epsilon/epsilon.tar.gz https://storage.googleapis.com/testdrive-templates/library/release/calm/epsilon.tar.gz'

# Remove the old docker images
ssh nutanix@$PC_IP "docker image rm \$(docker image ls | grep nucalm | awk '{print \$3}')"
ssh nutanix@$PC_IP "docker image rm \$(docker image ls | grep epsilon | awk '{print \$3}')"

# Start the services back up
ssh nutanix@$PC_IP 'source /etc/profile; cluster start'
