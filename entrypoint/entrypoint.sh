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
python3 calm_create_image.py
#python3 calm_enable_marketplace.py
python3 calm_upload_icons.py
sleep 1500 # sleep so the image can be created
python3 calm_create_project.py NY_Office LA_Office
python3 calm_create_env.py
python3 calm_configure_project.py
python3 calm_upload_bp.py
python3 calm_configure_bp.py
python3 calm_publish_bp.py
python3 calm_approve_bp.py
python3 calm_publish_apps.py
