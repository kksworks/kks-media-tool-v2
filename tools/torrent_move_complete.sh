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

#절대경로로 적는다.

DIR_1_ORIG="/mnt/250G_temp_disk/Torrent_Download_Complete/"
DIR_1_TARG="/mnt/5T_1_media_disk/download"

DIR_2_ORIG="/mnt/5T_1_media_disk/move_dir/move_to_5T_2/"
DIR_2_TARG="/mnt/5T_2_media_disk/temp"

DIR_3_ORIG="/mnt/5T_1_media_disk/move_dir/move_to_5T_3/"
DIR_3_TARG="/mnt/5T_3_media_disk/temp"

DIR_4_ORIG="/mnt/5T_1_media_disk/move_dir/move_to_5T_4/"
DIR_4_TARG="/mnt/5T_4_media_disk/temp"

MOVE_DIR_ORIG=(${DIR_1_ORIG} ${DIR_2_ORIG} ${DIR_3_ORIG} ${DIR_4_ORIG})
MOVE_DIR_TARG=(${DIR_1_TARG} ${DIR_2_TARG} ${DIR_3_TARG} ${DIR_4_TARG})

#-------------------------------------------------------
#INOTIFY_WATCH_DIR=${DIR_1_ORIG}
INOTIFY_WATCH_DIR=${MOVE_DIR_ORIG[@]}
INOTIFY_TIMEOUT_SEC=600
#-------------------------------------------------------

move_func()
{
    MOVE_SRC=$1
    MOVE_TARG=$2
    if [ ! -d "${MOVE_TARG}" ]; then
        mkdir -p ${MOVE_TARG}
        # Control will enter here if $DIRECTORY doesn't exist.
    fi
    /usr/bin/rsync --remove-source-files --force -rvh ${MOVE_SRC} ${MOVE_TARG}
#    rm -rf ${DIR_1_ORIG}*
    find ${MOVE_SRC} -mindepth 1 -type d -empty -exec rmdir "{}" \;
}



func_file_move()
{
    echo "start copy"

    for index in ${!MOVE_DIR_ORIG[*]} ; do
        move_func ${MOVE_DIR_ORIG[$index]} ${MOVE_DIR_TARG[$index]}
    done

    ## torrent_del_complete.sh zzzz

#    chmod 777 -R ${TORRENT_COMPLETE_DIR}
#    mv -f ${TORRENT_COMPLETE_DIR}/* ${TORRENT_COMPLETE_DIR_CPY}
 #   rm -rf ${TORRENT_COMPLETE_DIR}/*
 #   /usr/bin/rsync --remove-source-files -rvh ${TORRENT_COMPLETE_DIR} ${TORRENT_COMPLETE_DIR_CPY}
    #find ${TORRENT_COMPLETE_DIR} -depth -type d 1 -empty -delete
 #   mkdir ${TORRENT_COMPLETE_DIR}


#    mv -f ${MOVE_TO_DISK_2_SRC}/* ${MOVE_TO_DISK_2_TARG}
#    /usr/bin/rsync --remove-source-files -rvh ${MOVE_TO_DISK_2_SRC} ${MOVE_TO_DISK_2_TARG}
 #   find ${MOVE_TO_DISK_2_SRC} -depth -type d -empty -delete
 #   rm -rf ${MOVE_TO_DISK_2_SRC}/*

 #   mv -f ${MOVE_TO_DISK_3_SRC}/* ${MOVE_TO_DISK_3_TARG}
 #   /usr/bin/rsync --remove-source-files -rvh ${MOVE_TO_DISK_3_SRC} ${MOVE_TO_DISK_3_TARG}
#    find ${MOVE_TO_DISK_3_SRC} -depth -type d -empty -delete
#  rm -rf ${MOVE_TO_DISK_3_SRC}/*
}

# --------------------
# check new file
# --------------------

while true; do

inotifywait --timeout ${INOTIFY_TIMEOUT_SEC} -e create -e moved_to -r ${INOTIFY_WATCH_DIR} && func_file_move
func_file_move

done

