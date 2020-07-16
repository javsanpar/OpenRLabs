#!/bin/bash

read -p "Enter Server RLABS IP or Domain: " server_rlabs

if [ "$server_rlabs" = "" ]; then
	echo "Server IP or Domain is needed as argument"
	exit 0
fi

read -p "Enter proxy PORT Secure WebSocket Guacamole [default 8020] : " port_wss

port_wss=${port_wss:-8020}

read -p "Enter Server Guacamole IP or Domain [default $server_rlabs] : " server_guac

server_guac=${server_guac:-$server_rlabs}


read -p "Enter PORT WebSocket Guacamole [default 8080] : " port_ws

port_ws=${port_ws:-8080}


echo "+------------------------------------------+"
echo "|                                          |"
echo "|         Configuring NGINX                |"
echo "|                                          |"
echo "+------------------------------------------+"

tar xzf packages/nginx_config.tar.gz -C packages/

w2pdir=$(cat /tmp/w2p_dir.tmp)


echo "SERVER_RLABS=$server_rlabs" >> $w2pdir/setup_init.cfg
echo "PORT_WSS=$port_wss" >> $w2pdir/setup_init.cfg
echo "SERVER_GUAC=$server_guac" >> $w2pdir/setup_init.cfg
echo "PORT_WS=$port_ws" >> $w2pdir/setup_init.cfg

w2pdir_scaped=$(echo $w2pdir | sed 's/\//\\\//g')

sed -i "s/\$SERVER_RLABS/$server_rlabs/g; 
	s/\$PORT_WSS/$port_wss/g; 
	s/\$SERVER_GUAC/$server_guac/g; 
	s/\$PORT_WS/$port_ws/g; 
	s/\$W2PDIR/$w2pdir_scaped/g"  packages/nginx_config/sites-available/web2py

cp packages/nginx_config/sites-available/web2py /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/web2py  /etc/nginx/sites-enabled/web2py
ln -s /etc/nginx/sites-available/default  /etc/nginx/sites-enabled/default

rm -fr packages/nginx_config

mkdir /etc/nginx/ssl
cp $w2pdir/certs/* /etc/nginx/ssl/

systemctl restart nginx.service

