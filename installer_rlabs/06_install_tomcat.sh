#!/bin/bash
. utils/package_manager.sh

echo "+------------------------------------------+"
echo "|                                          |"
echo "|         Installing TOMCAT8               |"
echo "|                                          |"
echo "+------------------------------------------+"

$pkg_mng --yes install tomcat8 tomcat8-admin 

