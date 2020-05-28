#!/bin/bash
. utils/package_manager.sh

echo "+------------------------------------------+"
echo "|                                          |"
echo "|         Installing GUACD                 |"
echo "|                                          |"
echo "+------------------------------------------+"




tar xzf packages/guacamole-server-1.1.0.tar.gz -C packages/
cd packages/guacamole-server-1.1.0/

$pkg_mng --yes install libcairo2  libpango1.0-dev libjpeg-dev libossp-uuid-dev libssh2-1-dev freerdp2-dev libwebsockets-dev \
						 libwebp-dev libavcodec-dev libavutil-dev libswscale-dev libvorbis-dev libpulse-dev

./configure --with-systemd-dir=/lib/systemd/system/

make && make install
ldconfig

groupadd guacd
useradd -r guacd -m -d /var/run/guacd -s /bin/nologin -g guacd -c guacd 

sed -i s/User=daemon/User=guacd/ /lib/systemd/system/guacd.service

systemctl enable guacd.service
systemctl start guacd.service

