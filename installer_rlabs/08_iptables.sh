#!/bin/bash
. utils/package_manager.sh

echo "+------------------------------------------+"
echo "|                                          |"
echo "|         Installing iptables              |"
echo "|                                          |"
echo "+------------------------------------------+"

$pkg_mng --yes install iptables

echo "+------------------------------------------+"
echo "|                                          |"
echo "|         Installing at program            |"
echo "|                                          |"
echo "+------------------------------------------+"

$pkg_mng --yes install at




echo "+------------------------------------------+"
echo "|                                          |"
echo "|         Config IP Forward                |"
echo "|                                          |"
echo "+------------------------------------------+"


sed -i s/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/g /etc/sysctl.conf
sed -i s/#net.ipv4.ip_forward=0/net.ipv4.ip_forward=1/g /etc/sysctl.conf

echo 1 > /proc/sys/net/ipv4/ip_forward


echo "+------------------------------------------+"
echo "|                                          |"
echo "|         Config sudo iptables, at         |"
echo "|                                          |"
echo "+------------------------------------------+"

echo "www-data ALL=(ALL) NOPASSWD: /sbin/iptables" >> /etc/sudoers
echo "www-data ALL=(ALL) NOPASSWD: /usr/bin/at" >> /etc/sudoers