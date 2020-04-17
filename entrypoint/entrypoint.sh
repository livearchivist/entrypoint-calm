#!/bin/bash
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
execute_command "export NUTEST_PATH=/home"
python3 pc_create_image.py
python3 pc_ntp.py
python3 pe_ntp.py
sleep 1200 # sleep so the image can be created
sh create_ssh_keys.sh
python3 pc_ssh_keys.py
sh copy_karbon_bits.sh
#python3 calm_create_env.py
#python3 calm_configure_project.py
#python3 calm_upload_bp.py
#python3 calm_configure_bp.py
#python3 calm_launch_bp.py
#sleep 1000
