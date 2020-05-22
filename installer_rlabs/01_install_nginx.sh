#!/bin/bash
. utils/package_manager.sh

echo "+------------------------------------------+"
echo "|                                          |"
echo "|         Installing NGINX                 |"
echo "|                                          |"
echo "+------------------------------------------+"

$pkg_mng --yes install nginx 
