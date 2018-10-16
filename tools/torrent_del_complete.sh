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


# port, username, password
SERVER="--auth ${TM_SETTING_ID}:${TM_SETTING_PASS}"

# use transmission-remote to get torrent list from transmission-remote list
# use sed to delete first / last line of output, and remove leading spaces
# use cut to get first field from each line
TORRENTLIST=`transmission-remote $SERVER --list | sed -e '1d;$d;s/^ *//' | cut --only-delimited --delimiter=" "  --fields=1`

# for each torrent in the list
for TORRENTID in $TORRENTLIST
do

# check if torrent download is completed
DL_COMPLETED=`transmission-remote $SERVER --torrent $TORRENTID --info | grep "Percent Done: 100%"`

# check torrentâ<80><99>s current state is
STATE_STOPPED=`transmission-remote $SERVER --torrent $TORRENTID --info | grep "State: Stopped\|Finished\|Idle"`

# if the torrent is "Stopped", "Finished", or "Idle after downloading 100%"
if [ "$DL_COMPLETED" ] && [ "$STATE_STOPPED" ]; then
    # move the files and remove the torrent from Transmission
    echo "Torrent #$TORRENTID is completed"
#    echo "Moving downloaded file(s) to $MOVEDIR"
#transmission-remote $SERVER --torrent $TORRENTID --move $MOVEDIR
    echo "Removing torrent from list"
   transmission-remote $SERVER --torrent $TORRENTID --remove
else
    echo "Torrent #$TORRENTID is not completed. Ignoring."
fi

done
