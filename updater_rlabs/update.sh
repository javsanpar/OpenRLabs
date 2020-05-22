#!/bin/bash

read -p "Enter rlabs directory [default:/var/www/web2py]: " w2p_dir
w2p_dir=${w2p_dir:-/var/www/web2py}


echo "+------------------------------------------+"
echo "|                                          |"
echo "|    Updating OPENRLABS WEB2PY APP       |"
echo "|                                          |"
echo "+------------------------------------------+"


tar -zcf web2py_rlabs_old.tar.gz $w2p_dir

tar -xf rlabs_update.tar.gz
cp -afR rlabs/* $w2p_dir/applications/rlabs/
chown -R www-data:www-data $w2p_dir/applications/rlabs/
rm -fr ./rlabs
