#/bin/bash


echo "+------------------------------------------+"
echo "|                                          |"
echo "|         Installing WEB2PY_RLABS          |"
echo "|                                          |"
echo "+------------------------------------------+"

sh 00_install_python.sh
sh 01_install_postgresql.sh
sh 01_install_nginx.sh
sh 02_install_web2py_rlabs.sh
sh 03_config_nginx.sh
sh 04_install_uwsgi.sh
