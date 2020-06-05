#!/bin/bash

read -p "Enter Server OPENGNSYS IP or Domain: " server_opengnsys

if [ "$server_opengnsys" = "" ]; then
	echo "Server OPENGNSYS IP or Domain is needed as argument"
	exit 0
fi

read -p "Enter rlabs directory [default:/var/www/web2py]: " w2p_dir
w2p_dir=${w2p_dir:-/var/www/web2py}

read -p "Enter Authentication Mail Pop Server: " pop3_server
read -p "Enter PORT pop server [default 110] : " port_pop3


port_pop3=${port_pop3:-110}

read -p "Use TLS in port server Yes/No [default No]: " use_tls

use_tls=${use_tls:-No}

if [ "$use_tls" != "Yes" ] && [ "$use_tls" != "No" ]; then
	echo "Use TLS must be Yes or No"
	exit 0
fi

read -p "Enter rlabs admin user [Example: foo@pop3.server.com]. \n ¡¡Important!! MUST BE able to authenticate against the POP3 SERVER: " admin_rlabs

if [ "$admin_rlabs" = "" ]; then
	echo "admin user is needed as argument"
	exit 0
fi


echo $w2p_dir > tmp/w2p_dir.tmp 

echo "+------------------------------------------+"
echo "|                                          |"
echo "|    Installing OPENRLABS WEB2PY APP       |"
echo "|                                          |"
echo "+------------------------------------------+"


tar xf packages/web2py_rlabs.tar.gz -C packages/
rm -fr $wsp_dir
mv ./packages/web2py_rlabs $w2p_dir


echo "SERVER_OPENGNSYS=$server_opengnsys" > $w2p_dir/setup_init.cfg
echo "POP3_SERVER=$pop3_server" >> $w2p_dir/setup_init.cfg
echo "PORT_POP3_SERVER=$port_pop3" >> $w2p_dir/setup_init.cfg
echo "USE_TLS=$use_tls" >> $w2p_dir/setup_init.cfg
echo "ADMIN_RLABS=$admin_rlabs" >> $w2p_dir/setup_init.cfg

chown -R www-data.www-data $w2p_dir
rm -fr packages/web2py_rlabs

