#!/bin/bash


echo "+------------------------------------------+"
echo "|                                          |"
echo "|         Installing UWSGI                 |"
echo "|                                          |"
echo "+------------------------------------------+"

pip3 install uwsgi


tar xf packages/uwsgi.tar.gz -C packages/

w2p_dir=$(cat tmp/w2p_dir.tmp)
w2p_dir_scaped=$(echo $w2p_dir | sed 's/\//\\\//g')
sed -i -e "s/\$W2P_DIR/$w2p_dir_scaped/g"  packages/uwsgi/sites/web2py.ini

mkdir -p /etc/uwsgi/sites/
cp  packages/uwsgi/sites/web2py.ini /etc/uwsgi/sites/

cp packages/uwsgi/uwsgi.service /etc/systemd/system/
systemctl enable uwsgi.service
systemctl start uwsgi.service

rm -fr packages/uwsgi
