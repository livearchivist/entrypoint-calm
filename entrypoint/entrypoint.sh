#!/bin/bash
set -e
function execute_command {
    echo "Executing: $@"
    eval $@
    rc=$?
    echo "Done"
    echo
    return $rc
}

cd "$(dirname "$0")"
echo ${CUSTOM_SCRIPT_CONFIG}
yum -y install epel-release
yum -y install $(cat yum_pkgs.txt)
pip3 install -r requirements.txt
python3 pc_create_image.py
sleep 300
python3 calm_create_env.py
python3 calm_configure_project.py
