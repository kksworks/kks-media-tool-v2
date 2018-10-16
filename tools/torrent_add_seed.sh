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

SEED_ROOT="/mnt/250G_temp_disk/Torrent_Seed"

check_trans_daemon_service()
{
        STAT_TM=`service transmission-daemon status`
        flag=`echo $STAT_TM | grep -c "not" `
        echo flag is $flag
        if [ ${flag} -gt 0 ]
        then
                echo "trans mission not running"
                STAT_TM=`service transmission-daemon restart`
        else
                echo "trans mission running"
        fi
}


func_add_seed ()
{

        echo "$1"

#       find $1 -print0 | while read -d $'\0' file
#       do
#         echo test !!!! $file
#       done

        #for f in "$(find $1 -name  '*.torrent')";
        find $1 -iname "*.torrent" | while read f
        do
                check_trans_daemon_service
                echo "add torrent : [ $f ] "
                TRANSMISSON_RESULT=`transmission-remote --auth ${TM_SETTING_ID}:${TM_SETTING_PASS} --add "$f" `
                flag=`echo $TRANSMISSON_RESULT |awk '{print match($0,"success")}'`;
                if [ $flag -gt 0 ]
                then
                        echo "torrent add success"
                        rm -rf "$f"
                else
                        echo "torrent add Fail";
                        rm -rf "$f"
                fi
        done
}

func_seek_seed()
{
    sleep 1
        func_add_seed ${SEED_ROOT}
}

# --------------------
# check new file
# --------------------

func_seek_seed

while true; do

inotifywait --timeout 300 -e create -e moved_to -r ${SEED_ROOT} && func_seek_seed
func_seek_seed

done

