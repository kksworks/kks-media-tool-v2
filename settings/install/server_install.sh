#!/bin/bash

unzip install_files.zip
echo "----------------------------------"
echo "import db info...\r\n"
echo "----------------------------------"
mysql -u root -p < ./install_files/sql/create_db.sql
mysql -u root -p torrent_mgr < ./install_files/sql/list_mgr_torrentlist.sql
mysql -u root -p torrent_mgr < ./install_files/sql/site_mgr_torrentsite.sql
mysql -u root -p torrent_mgr < ./install_files/sql/torrent_script_log.sql

echo "----------------------------------"
echo "copy script file.."
echo "----------------------------------"
cp -rf ./install_files/script/* ./../