#!/bin/bash


MAIN_WORK_DIR=/home/torrent_mgr
USER_CONFIG_FILE_NAME=user.config.env

MAIN_SETTING_DIR=${MAIN_WORK_DIR}/settings

KKS_WORK_PYTHON_PATH=${MAIN_WORK_DIR}/kks_modules

if [  -e ${MAIN_SETTING_DIR}/${USER_CONFIG_FILE_NAME} ]
then
    echo "target env file : ${MAIN_SETTING_DIR}/${USER_CONFIG_FILE_NAME}"
    source ${MAIN_SETTING_DIR}/${USER_CONFIG_FILE_NAME}
else
    echo "target env file : ~/${USER_CONFIG_FILE_NAME}"
    source ~/${USER_CONFIG_FILE_NAME}
fi

#---------------------------------
TM_SETTING_ID=${USER_CONF__TRANSMISSION_ID}
TM_SETTING_PASS=${USER_CONF__TRANSMISSION_PW}
#---------------------------------

# move sub dir in files
find ${TR_TORRENT_DIR} -mindepth 2 -name "*.mp4"  -exec mv {} ${TR_TORRENT_DIR} \;
find ${TR_TORRENT_DIR} -mindepth 2 -name "*.avi"  -exec mv {} ${TR_TORRENT_DIR} \;
find ${TR_TORRENT_DIR} -mindepth 2 -name "*.mkv"  -exec mv {} ${TR_TORRENT_DIR} \;

# remove sub dir..
find ${TR_TORRENT_DIR} -mindepth 1 -type d -exec rm -r {} \;

# file name remove
find ${TR_TORRENT_DIR} -name "* *" -execdir rename 's/ //g' "{}" \;

# remove complete torrent
$MAIN_WORK_DIR/tools/torrent_del_complete.sh




