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
yum -y install $(cat yum_pkgs.txt)
pip3 install -r requirements.txt
execute_command "export NUTEST_PATH=/home"
python3 pc_create_image.py
python3 pc_ntp.py
python3 pe_ntp.py
python3 calm_upload_icons.py
python3 calm_enable_marketplace.py
python3 calm_enable_showback.py
sleep 1200 # sleep so the image can be created
sh create_ssh_keys.sh
python3 pc_ssh_keys.py
python pc_deploy_autodc.py
python3 calm_create_project.py NY_Office LA_Office
python3 calm_create_env.py
python3 calm_configure_project.py
python3 calm_upload_bp.py
python3 calm_configure_bp.py
python3 calm_launch_bp.py calm_bp_launch.json
python3 calm_publish_bp.py
python3 calm_approve_bp.py
python3 calm_publish_apps.py
python3 pc_authconfig.py
sleep 1200
python3 calm_launch_bp.py calm_bp_launch_depend.json
sleep 1200
python3 calm_check_apps.py
