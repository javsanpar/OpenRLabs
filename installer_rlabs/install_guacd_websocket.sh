#/bin/bash


echo "+------------------------------------------+"
echo "|                                          |"
echo "|         Installing GUACD WEBSOCKET       |"
echo "|                                          |"
echo "+------------------------------------------+"

sh 05_install_guacd.sh
sh 06_install_tomcat.sh
sh 07_install_websocket.sh
