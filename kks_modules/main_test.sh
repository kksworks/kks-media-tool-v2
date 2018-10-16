
#!/bin/bash

MAIN_WORK_DIR=/home/torrent_mgr
MAIN_SETTING_DIR=${MAIN_WORK_DIR}/settings
USER_CONFIG_FILE_NAME=user.config.env
KKS_WORK_PYTHON_PATH=${MAIN_WORK_DIR}/kks_modules

if [  -e ${MAIN_SETTING_DIR}/${USER_CONFIG_FILE_NAME} ]
then
    echo "target env file : ${MAIN_SETTING_DIR}/${USER_CONFIG_FILE_NAME}"
    source ${MAIN_SETTING_DIR}/${USER_CONFIG_FILE_NAME}
else
    echo "target env file : ~/${USER_CONFIG_FILE_NAME}"
    source ~/${USER_CONFIG_FILE_NAME}
fi

echo ${USER_CONF__DB_INFO__TORRENT_LOG__ID}
${KKS_WORK_PYTHON_PATH}/main_test.py


