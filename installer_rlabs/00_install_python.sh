#!/bin/bash
. utils/package_manager.sh

echo "+------------------------------------------+"
echo "|                                          |"
echo "|         Installing python3               |"
echo "|                                          |"
echo "+------------------------------------------+"

$pkg_mng --yes install python3 python3-pip

