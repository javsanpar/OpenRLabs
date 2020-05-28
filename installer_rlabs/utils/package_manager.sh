#!/bin/bash

if [ -f /etc/os-release ]; then
       	. /etc/os-release
	OS=$NAME
elif [ -f /etc/lsb-release ]; then
	. /etc/lsb-release
	OS=$DISTRIB_ID
fi

case $OS in
  Ubuntu | Debian)
	pkg_mng=apt
	;;
  RedHat | RHEL| CentOS)
	pkg_mng=yum 
	;;
  Fedora)
	pkg_mng=dnf
	;;
esac

